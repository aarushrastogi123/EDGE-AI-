import numpy as np
import tensorflow as tf


def load_tflite_model(tflite_path: str) -> tf.lite.Interpreter:
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    return interpreter


def preprocess_image(image, image_size: int, dtype=np.float32):
    image = tf.image.resize(image, [image_size, image_size])
    image = tf.cast(image, tf.float32) / 255.0
    image = tf.expand_dims(image, axis=0)
    return image.numpy().astype(dtype)


def predict(interpreter: tf.lite.Interpreter, image, image_size: int):
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]
    dtype = input_details["dtype"]
    data = preprocess_image(image, image_size, dtype=dtype)

    if input_details.get("quantization") and input_details["quantization"] != (0.0, 0):
        scale, zero_point = input_details["quantization"]
        data = data / scale + zero_point
        data = np.clip(data, np.iinfo(dtype).min, np.iinfo(dtype).max).astype(dtype)

    interpreter.set_tensor(input_details["index"], data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details["index"])
    probabilities = output_data.squeeze()
    prediction = int(np.argmax(probabilities))
    return prediction, probabilities.tolist()
