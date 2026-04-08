#!/usr/bin/env python3
"""Quick test to verify all connections and datasets are working."""

import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'EdgeVisionNet'))

import tensorflow as tf
from utils.config import get_config
from training.train import load_and_prepare_dataset

def test_tensorflow():
    print("=" * 60)
    print("1. Testing TensorFlow Installation")
    print("=" * 60)
    print(f"[OK] TensorFlow version: {tf.__version__}")

    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"[OK] GPU detected: {len(gpus)} GPU(s)")
        for gpu in gpus:
            print(f"  - {gpu}")
    else:
        print("[WARN] No GPU detected (CPU only - training will be slower)")
    print()

def test_config():
    print("=" * 60)
    print("2. Testing Configuration")
    print("=" * 60)
    config = get_config()
    print(f"[OK] Image size: {config.IMAGE_SIZE}x{config.IMAGE_SIZE}")
    print(f"[OK] Batch size: {config.BATCH_SIZE}")
    print(f"[OK] Epochs: {config.EPOCHS}")
    print(f"[OK] Dataset: {config.DATASET_NAME}")
    print(f"[OK] Models: {', '.join(config.MODEL_NAMES)}")
    print()

def test_dataset():
    print("=" * 60)
    print("3. Testing CIFAR-10 Dataset Loading")
    print("=" * 60)

    print("Loading dataset (first time will download ~170MB)...")
    start = time.time()

    try:
        train_ds, val_ds, test_ds, (x_test, y_test) = load_and_prepare_dataset()
        load_time = time.time() - start

        print(f"[OK] Dataset loaded in {load_time:.2f}s")
        print(f"[OK] Test set size: {len(x_test)} images")
        print()

        # Check one batch
        print("Checking batch shapes...")
        for images, labels in train_ds.take(1):
            print(f"[OK] Batch shape: {images.shape}")
            print(f"[OK] Labels shape: {labels.shape}")
        print()

    except Exception as e:
        print(f"[ERROR] Error loading dataset: {e}")
        return False

    return True

def test_models():
    print("=" * 60)
    print("4. Testing Model Building")
    print("=" * 60)

    from models.mobilenet import build_mobilenet
    from models.efficientnet import build_efficientnet
    from models.edgevisionnet import build_edgevisionnet

    config = get_config()
    input_shape = (config.IMAGE_SIZE, config.IMAGE_SIZE, 3)

    try:
        print("Building MobileNetV2...")
        m1 = build_mobilenet(input_shape, config.NUM_CLASSES, config.LEARNING_RATE)
        print(f"[OK] MobileNetV2 built - {m1.count_params():,} parameters")

        print("Building EfficientNetB0...")
        m2 = build_efficientnet(input_shape, config.NUM_CLASSES, config.LEARNING_RATE)
        print(f"[OK] EfficientNetB0 built - {m2.count_params():,} parameters")

        print("Building EdgeVisionNet...")
        m3 = build_edgevisionnet(input_shape, config.NUM_CLASSES, config.LEARNING_RATE)
        print(f"[OK] EdgeVisionNet built - {m3.count_params():,} parameters")
        print()

    except Exception as e:
        print(f"[ERROR] Error building models: {e}")
        return False

    return True

if __name__ == "__main__":
    test_tensorflow()
    test_config()
    dataset_ok = test_dataset()
    models_ok = test_models()

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if dataset_ok and models_ok:
        print("[OK] All tests passed! Ready to train.")
        print("\nTo start training, run:")
        print("  python EdgeVisionNet/main.py")
        print(f"\nExpected training time: ~2-3 minutes per model (5 epochs each)")
    else:
        print("[ERROR] Some tests failed. Please check the errors above.")
