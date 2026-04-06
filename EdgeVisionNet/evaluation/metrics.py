import numpy as np
import tensorflow as tf


def compute_classification_metrics(y_true, y_pred, num_classes: int):
    y_true = np.asarray(y_true).flatten()
    y_pred = np.asarray(y_pred).flatten()
    cm = tf.math.confusion_matrix(y_true, y_pred, num_classes=num_classes).numpy()

    true_positives = np.diag(cm)
    false_positives = np.sum(cm, axis=0) - true_positives
    false_negatives = np.sum(cm, axis=1) - true_positives

    precision_per_class = np.divide(
        true_positives,
        true_positives + false_positives + 1e-9,
    )
    recall_per_class = np.divide(
        true_positives,
        true_positives + false_negatives + 1e-9,
    )
    f1_per_class = np.divide(
        2 * precision_per_class * recall_per_class,
        precision_per_class + recall_per_class + 1e-9,
    )

    accuracy = np.sum(true_positives) / np.sum(cm)
    precision = np.mean(precision_per_class)
    recall = np.mean(recall_per_class)
    f1_score = np.mean(f1_per_class)

    metrics = {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1_score),
        "confusion_matrix": cm,
        "precision_per_class": precision_per_class.tolist(),
        "recall_per_class": recall_per_class.tolist(),
        "f1_per_class": f1_per_class.tolist(),
    }
    return metrics


def format_classification_report(metrics: dict, class_names: list) -> str:
    report_lines = ["Classification Report:\n"]
    report_lines.append(f"Overall Accuracy: {metrics['accuracy']:.4f}")
    report_lines.append(f"Macro Precision: {metrics['precision']:.4f}")
    report_lines.append(f"Macro Recall: {metrics['recall']:.4f}")
    report_lines.append(f"Macro F1 Score: {metrics['f1_score']:.4f}\n")
    report_lines.append("Class-wise metrics:")
    report_lines.append("class,precision,recall,f1_score")
    for idx, class_name in enumerate(class_names):
        report_lines.append(
            f"{class_name},{metrics['precision_per_class'][idx]:.4f},{metrics['recall_per_class'][idx]:.4f},{metrics['f1_per_class'][idx]:.4f}"
        )
    return "\n".join(report_lines)
