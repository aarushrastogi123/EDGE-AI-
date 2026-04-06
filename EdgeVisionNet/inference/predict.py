import tensorflow as tf


def load_keras_model(model_path: str) -> tf.keras.Model:
    return tf.keras.models.load_model(model_path)


def preprocess_image(image, image_size: int):
    image = tf.image.resize(image, [image_size, image_size])
    image = tf.cast(image, tf.float32) / 255.0
    return tf.expand_dims(image, axis=0)


def predict(model, image, image_size: int):
    image = preprocess_image(image, image_size)
    probabilities = model.predict(image, verbose=0)
    prediction = tf.argmax(probabilities, axis=-1).numpy()[0]
    return prediction, probabilities[0].tolist()
