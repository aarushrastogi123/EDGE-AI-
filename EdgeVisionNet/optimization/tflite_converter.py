import os
import tensorflow as tf


def convert_saved_model_to_tflite(saved_model_dir: str, output_path: str, quantize: bool = False, representative_dataset=None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    if quantize:
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        if representative_dataset is not None:
            converter.representative_dataset = representative_dataset
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.uint8
        converter.inference_output_type = tf.uint8
    tflite_model = converter.convert()

    with open(output_path, "wb") as f:
        f.write(tflite_model)

    return output_path
