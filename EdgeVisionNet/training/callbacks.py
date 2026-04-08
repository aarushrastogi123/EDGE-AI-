import os
import tensorflow as tf


def get_training_callbacks(model_name: str, results_dir: str, monitor: str = "val_loss"):
    checkpoint_filepath = os.path.join(results_dir, f"{model_name}_best.h5")
    os.makedirs(results_dir, exist_ok=True)

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor=monitor,
            patience=3,
            restore_best_weights=True,
            verbose=0,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_filepath,
            monitor=monitor,
            save_best_only=True,
            save_weights_only=False,
            verbose=0,
        ),
    ]
    return callbacks, checkpoint_filepath
