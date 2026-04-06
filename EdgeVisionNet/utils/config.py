import os


class Config:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(PROJECT_ROOT)

    DATASET_NAME = "CIFAR-10"
    IMAGE_SIZE = 224
    NUM_CLASSES = 10
    BATCH_SIZE = 64
    EPOCHS = 10
    LEARNING_RATE = 1e-3
    VALIDATION_SPLIT = 0.1
    SHUFFLE_BUFFER = 1024
    AUTOTUNE = -1
    MODEL_NAMES = ["mobilenetv2", "efficientnetb0", "edgevisionnet"]

    RESULTS_DIR = os.path.join(BASE_DIR, "results")
    GRAPH_DIR = os.path.join(RESULTS_DIR, "graphs")
    REPORT_DIR = os.path.join(RESULTS_DIR, "reports")
    MODEL_DIR = os.path.join(RESULTS_DIR, "models")
    TFLITE_DIR = os.path.join(RESULTS_DIR, "models")

    EARLY_STOPPING_PATIENCE = 3
    CHECKPOINT_MONITOR = "val_loss"
    CHECKPOINT_MODE = "min"
    VERBOSE = 1

    TFLITE_QUANTIZE = False
    TFLITE_QUANTIZE_INT8 = False
    TFLITE_NUM_CALIBRATION_STEPS = 100

    SEED = 42


def get_config() -> Config:
    return Config
