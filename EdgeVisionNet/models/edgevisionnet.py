import tensorflow as tf
from tensorflow.keras import layers, models


def channel_attention_block(inputs: tf.Tensor, reduction_ratio: int = 8) -> tf.Tensor:
    channel = inputs.shape[-1]
    x = layers.GlobalAveragePooling2D()(inputs)
    x = layers.Dense(channel // reduction_ratio, activation="relu")(x)
    x = layers.Dense(channel, activation="sigmoid")(x)
    x = layers.Reshape((1, 1, channel))(x)
    return layers.Multiply()([inputs, x])


def build_edgevisionnet(input_shape: tuple, num_classes: int, learning_rate: float) -> tf.keras.Model:
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights=None,
        pooling=None,
    )
    base_model.trainable = True

    inputs = layers.Input(shape=input_shape)
    x = base_model(inputs, training=True)
    x = channel_attention_block(x, reduction_ratio=8)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(512, activation="relu")(x)
    x = layers.Dropout(0.4)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="EdgeVisionNet")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model
