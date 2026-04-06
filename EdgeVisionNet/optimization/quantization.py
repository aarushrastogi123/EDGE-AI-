import tensorflow as tf


def representative_dataset_generator(dataset):
    for image, _ in dataset:
        yield [tf.cast(image, tf.float32)]


def apply_quantization(model_path: str, representative_dataset, output_tflite_path: str, int8: bool = False):
    converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    if representative_dataset is not None:
        converter.representative_dataset = representative_dataset
    if int8:
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.uint8
        converter.inference_output_type = tf.uint8
    tflite_model = converter.convert()

    with open(output_tflite_path, "wb") as f:
        f.write(tflite_model)
    return output_tflite_path
