import os
import json
import numpy as np
import tensorflow as tf

from utils.config import get_config
from utils.logger import get_logger
from models.mobilenet import build_mobilenet
from models.efficientnet import build_efficientnet
from models.edgevisionnet import build_edgevisionnet
from training.train import (
    load_and_prepare_dataset,
    train_model,
    save_history_plot,
    build_dataset_for_tflite,
)
from evaluation.metrics import compute_classification_metrics, format_classification_report
from evaluation.confusion_matrix import plot_confusion_matrix
from evaluation.latency import measure_latency_tf
from inference.predict import predict
from inference.tflite_inference import load_tflite_model, predict as predict_tflite
from optimization.tflite_converter import convert_saved_model_to_tflite


config = get_config()
logger = get_logger("EdgeVisionNet")
CLASS_NAMES = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]


def ensure_directories():
    os.makedirs(config.GRAPH_DIR, exist_ok=True)
    os.makedirs(config.REPORT_DIR, exist_ok=True)
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    os.makedirs(config.TFLITE_DIR, exist_ok=True)


def build_model(model_name: str):
    input_shape = (config.IMAGE_SIZE, config.IMAGE_SIZE, 3)
    if model_name == "mobilenetv2":
        return build_mobilenet(input_shape, config.NUM_CLASSES, config.LEARNING_RATE)
    if model_name == "efficientnetb0":
        return build_efficientnet(input_shape, config.NUM_CLASSES, config.LEARNING_RATE)
    if model_name == "edgevisionnet":
        return build_edgevisionnet(input_shape, config.NUM_CLASSES, config.LEARNING_RATE)
    raise ValueError(f"Unknown model name: {model_name}")


def evaluate_model(model, test_ds, class_names, model_name: str):
    logger.info(f"Evaluating {model_name} on test dataset.")
    y_true = []
    y_pred = []
    for x_batch, y_batch in test_ds:
        probabilities = model.predict(x_batch, verbose=0)
        predictions = np.argmax(probabilities, axis=-1)
        y_true.extend(y_batch.numpy().tolist())
        y_pred.extend(predictions.tolist())

    metrics = compute_classification_metrics(y_true, y_pred, num_classes=config.NUM_CLASSES)
    report_text = format_classification_report(metrics, class_names)
    report_path = os.path.join(config.REPORT_DIR, f"{model_name}_classification_report.txt")
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(report_text)

    cm_path = os.path.join(config.GRAPH_DIR, f"{model_name}_confusion_matrix.png")
    plot_confusion_matrix(metrics["confusion_matrix"], class_names, cm_path)
    logger.info(f"Saved classification report to {report_path}")
    logger.info(f"Saved confusion matrix to {cm_path}")
    return metrics


def save_comparison_table(comparison_data):
    table_path = os.path.join(config.REPORT_DIR, "model_comparison_table.md")
    with open(table_path, "w", encoding="utf-8") as table_file:
        table_file.write("# Model Comparison\n\n")
        table_file.write("| Model | Accuracy | Precision | Recall | F1 Score | Size (MB) | Latency (ms) | FPS |\n")
        table_file.write("|---|---|---|---|---|---|---|---|\n")
        for item in comparison_data:
            table_file.write(
                f"| {item['model']} | {item['accuracy']:.4f} | {item['precision']:.4f} | {item['recall']:.4f} | {item['f1_score']:.4f} | {item['size_mb']:.2f} | {item['latency_ms']:.4f} | {item['fps']:.2f} |\n"
            )
    logger.info(f"Saved model comparison table to {table_path}")
    return table_path


def save_latency_report(latency_data):
    report_path = os.path.join(config.REPORT_DIR, "latency_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(latency_data, f, indent=2)
    logger.info(f"Saved latency report to {report_path}")
    return report_path


def save_model_artifact(model, model_name: str):
    model_export_path = os.path.join(config.MODEL_DIR, f"{model_name}_saved_model")
    model.save(model_export_path, include_optimizer=False)
    return model_export_path


def run_inference_examples(model, tflite_path, x_test):
    sample_image = x_test[0]
    keras_prediction, keras_probs = predict(model, sample_image, config.IMAGE_SIZE)
    logger.info(f"Keras inference sample prediction: {keras_prediction}, scores: {keras_probs[:3]}...")

    if tflite_path and os.path.exists(tflite_path):
        interpreter = load_tflite_model(tflite_path)
        tflite_prediction, tflite_probs = predict_tflite(interpreter, sample_image, config.IMAGE_SIZE)
        logger.info(f"TFLite inference sample prediction: {tflite_prediction}, scores: {tflite_probs[:3]}...")
        return keras_prediction, tflite_prediction
    return keras_prediction, None


def main():
    ensure_directories()
    logger.info("Starting EdgeVisionNet pipeline.")

    train_ds, val_ds, test_ds, (x_test, y_test) = load_and_prepare_dataset()
    comparison_data = []
    benchmark_results = {}

    for model_name in config.MODEL_NAMES:
        logger.info(f"Building {model_name}.")
        model = build_model(model_name)

        history, checkpoint_path = train_model(model, train_ds, val_ds, model_name)
        save_history_plot(history, model_name, config.GRAPH_DIR)

        logger.info(f"Loading best checkpoint from {checkpoint_path}.")
        best_model = tf.keras.models.load_model(checkpoint_path)
        saved_model_dir = save_model_artifact(best_model, model_name)

        metrics = evaluate_model(best_model, test_ds, CLASS_NAMES, model_name)
        latency = measure_latency_tf(best_model, test_ds, num_samples=100)
        model_size = os.path.getsize(checkpoint_path) / 1_000_000.0

        comparison_data.append(
            {
                "model": model_name,
                "accuracy": metrics["accuracy"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1_score"],
                "size_mb": model_size,
                "latency_ms": latency["average_latency_seconds"] * 1000.0,
                "fps": latency["frames_per_second"],
            }
        )
        benchmark_results[model_name] = {
            "checkpoint_path": checkpoint_path,
            "saved_model_dir": saved_model_dir,
            "metrics": metrics,
            "latency": latency,
        }

    comparison_table_path = save_comparison_table(comparison_data)
    latency_report_path = save_latency_report({name: benchmark_results[name]["latency"] for name in benchmark_results})

    best_model_name = max(comparison_data, key=lambda x: x["accuracy"])["model"]
    logger.info(f"Selecting best model for edge optimization: {best_model_name}")
    best_saved_model_dir = benchmark_results[best_model_name]["saved_model_dir"]
    output_tflite_path = os.path.join(config.TFLITE_DIR, f"{best_model_name}.tflite")

    representative_ds = build_dataset_for_tflite(x_test, y_test, sample_count=config.TFLITE_NUM_CALIBRATION_STEPS)
    convert_saved_model_to_tflite(
        saved_model_dir=best_saved_model_dir,
        output_path=output_tflite_path,
        quantize=config.TFLITE_QUANTIZE,
        representative_dataset=representative_ds if config.TFLITE_QUANTIZE else None,
    )
    logger.info(f"Saved TFLite model at {output_tflite_path}")

    best_model = tf.keras.models.load_model(benchmark_results[best_model_name]["checkpoint_path"])
    run_inference_examples(best_model, output_tflite_path, x_test)

    logger.info("EdgeVisionNet pipeline completed successfully.")
    logger.info(f"Reports are available in {config.REPORT_DIR}")
    logger.info(f"Graphs are available in {config.GRAPH_DIR}")
    logger.info(f"Model artifacts are available in {config.MODEL_DIR}")
    logger.info(f"TFLite artifacts are available in {config.TFLITE_DIR}")


if __name__ == "__main__":
    main()
