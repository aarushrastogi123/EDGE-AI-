import tensorflow as tf


def channel_attention_block(inputs: tf.Tensor, reduction_ratio: int = 8) -> tf.Tensor:
    channel = inputs.shape[-1]
    x = tf.keras.layers.GlobalAveragePooling2D()(inputs)
    x = tf.keras.layers.Dense(channel // reduction_ratio, activation="relu")(x)
    x = tf.keras.layers.Dense(channel, activation="sigmoid")(x)
    x = tf.keras.layers.Reshape((1, 1, channel))(x)
    return tf.keras.layers.Multiply()([inputs, x])


def build_edgevisionnet(input_shape: tuple, num_classes: int, learning_rate: float) -> tf.keras.Model:
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights=None,
        pooling=None,
    )
    base_model.trainable = True

    inputs = tf.keras.layers.Input(shape=input_shape)
    x = base_model(inputs, training=True)
    x = channel_attention_block(x, reduction_ratio=8)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(512, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.4)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)

    model = tf.keras.models.Model(inputs=inputs, outputs=outputs, name="EdgeVisionNet")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model
