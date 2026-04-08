import os
import tensorflow as tf

from utils.config import get_config
from training.augment import get_augmentation_layer
from training.callbacks import get_training_callbacks

AUTOTUNE = tf.data.AUTOTUNE


config = get_config()


def preprocess_image(image, label):
    image = tf.image.resize(image, [config.IMAGE_SIZE, config.IMAGE_SIZE])
    image = tf.cast(image, tf.float32) / 255.0
    return image, label


def load_and_prepare_dataset():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    y_train = y_train.squeeze()
    y_test = y_test.squeeze()

    dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    dataset = dataset.shuffle(config.SHUFFLE_BUFFER, seed=config.SEED)
    total_train = len(x_train)
    val_count = int(total_train * config.VALIDATION_SPLIT)

    train_data = dataset.skip(val_count)
    val_data = dataset.take(val_count)

    # Pre-compute and cache preprocessing to avoid recomputation
    train_ds = (
        train_data.map(preprocess_image, num_parallel_calls=AUTOTUNE)
        .cache()
        .shuffle(config.SHUFFLE_BUFFER, seed=config.SEED)
        .batch(config.BATCH_SIZE)
        .prefetch(AUTOTUNE)
    )

    val_ds = (
        val_data.map(preprocess_image, num_parallel_calls=AUTOTUNE)
        .cache()
        .batch(config.BATCH_SIZE)
        .prefetch(AUTOTUNE)
    )

    test_ds = (
        tf.data.Dataset.from_tensor_slices((x_test, y_test))
        .map(preprocess_image, num_parallel_calls=AUTOTUNE)
        .batch(config.BATCH_SIZE)
        .prefetch(AUTOTUNE)
    )

    print(f"✓ Data loaded: {len(x_train)} train samples, {val_count} val samples, {len(x_test)} test samples")
    print(f"✓ Batch size: {config.BATCH_SIZE}, Image size: {config.IMAGE_SIZE}x{config.IMAGE_SIZE}")
    return train_ds, val_ds, test_ds, (x_test, y_test)


def build_dataset_for_tflite(images, labels, sample_count=100):
    ds = tf.data.Dataset.from_tensor_slices((images, labels))
    ds = ds.map(preprocess_image, num_parallel_calls=AUTOTUNE)
    ds = ds.batch(1).take(sample_count)
    return ds


def create_augmented_dataset(dataset):
    augmentation = get_augmentation_layer()
    return dataset.map(lambda x, y: (augmentation(x, training=True), y), num_parallel_calls=AUTOTUNE)


def train_model(model, train_ds, val_ds, model_name: str):
    callbacks, checkpoint_path = get_training_callbacks(
        model_name=model_name,
        results_dir=config.MODEL_DIR,
        monitor=config.CHECKPOINT_MONITOR,
    )

    print(f"\n{'='*60}")
    print(f"Training {model_name} for {config.EPOCHS} epochs")
    print(f"{'='*60}\n")

    history = model.fit(
        create_augmented_dataset(train_ds),
        validation_data=val_ds,
        epochs=config.EPOCHS,
        callbacks=callbacks,
        verbose=config.VERBOSE,
    )
    return history, checkpoint_path


def save_history_plot(history, model_name: str, graph_dir: str):
    import matplotlib.pyplot as plt

    os.makedirs(graph_dir, exist_ok=True)
    plt.figure(figsize=(8, 6))
    plt.plot(history.history["accuracy"], label="train_accuracy")
    plt.plot(history.history["val_accuracy"], label="val_accuracy")
    plt.title(f"{model_name} Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(graph_dir, f"{model_name}_accuracy.png"))
    plt.close()
