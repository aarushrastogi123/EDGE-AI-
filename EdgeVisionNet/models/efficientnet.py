import tensorflow as tf


def build_efficientnet(input_shape: tuple, num_classes: int, learning_rate: float) -> tf.keras.Model:
    base_model = tf.keras.applications.EfficientNetB0(
        input_shape=input_shape,
        include_top=False,
        weights=None,
        pooling=None,
    )
    base_model.trainable = True

    inputs = tf.keras.layers.Input(shape=input_shape)
    x = base_model(inputs, training=True)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(256, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.4)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)

    model = tf.keras.models.Model(inputs=inputs, outputs=outputs, name="EfficientNetB0_CIFAR10")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model
