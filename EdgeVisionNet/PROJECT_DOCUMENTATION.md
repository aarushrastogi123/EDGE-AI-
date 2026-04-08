# EdgeVisionNet Project Documentation

## Overview
EdgeVisionNet is a modular Edge AI research pipeline built around CIFAR-10 image classification. It includes:

- dataset loading and preprocessing
- data augmentation
- three model definitions: MobileNetV2, EfficientNet-B0, and a custom EdgeVisionNet
- full training loop with validation and early stopping
- evaluation with accuracy, precision, recall, F1 score, and confusion matrix
- latency benchmarking and FPS measurement
- TensorFlow Lite conversion with optional quantization
- inference via TensorFlow and TFLite
- report generation and artifact saving


## Project Structure

- `data/`
  - `raw/` and `processed/` directories are created for future dataset storage, but the current pipeline loads CIFAR-10 directly via TensorFlow.
- `models/`
  - `mobilenet.py` — baseline MobileNetV2 model
  - `efficientnet.py` — baseline EfficientNet-B0 model
  - `edgevisionnet.py` — custom EdgeVisionNet architecture built on MobileNetV2 with channel attention
- `training/`
  - `train.py` — dataset creation, preprocessing, augmentation, training loop, and plot saving
  - `augment.py` — augmentation pipeline with rotation, flip, zoom
  - `callbacks.py` — early stopping and model checkpoint callbacks
- `evaluation/`
  - `metrics.py` — compute accuracy, precision, recall, F1 score, and confusion matrix
  - `confusion_matrix.py` — plot confusion matrix
  - `latency.py` — measure TensorFlow and TFLite inference latency and FPS
- `optimization/`
  - `quantization.py` — helper for quantized TFLite conversion with representative dataset
  - `pruning.py` — optional pruning wrapper via TensorFlow Model Optimization
  - `tflite_converter.py` — save a TensorFlow SavedModel as a `.tflite` file
- `inference/`
  - `predict.py` — TensorFlow model inference pipeline
  - `tflite_inference.py` — TFLite interpreter inference pipeline
- `utils/`
  - `config.py` — pipeline configuration and hyperparameters
  - `logger.py` — logging setup for console output and report file
- `results/`
  - `graphs/` — accuracy plot output
  - `reports/` — classification reports, comparison tables, latency reports, logs
  - `models/` — saved model artifacts and `.tflite` files
- `main.py` — orchestrates the end-to-end process

## Step-by-Step Workflow

### 1. Configuration (`utils/config.py`)
This file controls all key pipeline parameters:

- `IMAGE_SIZE = 224`
- `BATCH_SIZE = 64`
- `EPOCHS = 10`
- `LEARNING_RATE = 1e-3`
- `VALIDATION_SPLIT = 0.1`
- `MODEL_NAMES = ["mobilenetv2", "efficientnetb0", "edgevisionnet"]`
- TFLite settings and result directories

This makes the pipeline easy to tune without editing core logic.

### 2. Dataset Loading and Preprocessing (`training/train.py`)
The pipeline:

- downloads CIFAR-10 using `tf.keras.datasets.cifar10.load_data()`
- squeezes label dimensions
- splits the training set into training and validation using `VALIDATION_SPLIT`
- resizes images to `224x224`
- normalizes pixel values to `[0, 1]`
- builds `tf.data` pipelines with caching, shuffling, batching, and prefetching

A separate helper generates a small calibration dataset for TFLite conversion.

### 3. Data Augmentation (`training/augment.py`)
This file defines an augmentation layer with:

- horizontal flips
- random rotation
- random zoom

The augmentation is applied only to training batches.

### 4. Models

#### `models/mobilenet.py`
Baseline MobileNetV2 architecture with:

- MobileNetV2 base (no top)
- GlobalAveragePooling
- Dense(256, relu)
- Dropout(0.4)
- Softmax output

#### `models/efficientnet.py`
Baseline EfficientNetB0 architecture with a similar top block.

#### `models/edgevisionnet.py`
Custom research model built on MobileNetV2 with:

- channel attention block using global pooling and dense gating
- a deeper dense head with 512 units
- dropout and softmax classification

This is the core EdgeVisionNet research contribution.

### 5. Training System
The training loop:

- builds the selected model
- applies augmentation to the training dataset
- validates on a held-out split
- uses early stopping and checkpoint saving
- saves training and validation accuracy plots in `results/graphs/`

### 6. Callbacks (`training/callbacks.py`)
Callbacks include:

- `EarlyStopping` monitoring `val_loss`
- `ModelCheckpoint` saving the best model

This ensures training stops early on plateau and preserves the best weights.

### 7. Evaluation

#### Metrics (`evaluation/metrics.py`)
Computes:
- accuracy
- precision
- recall
- macro F1 score
- confusion matrix

Also formats a textual classification report written to `results/reports/`.

#### Confusion Matrix Plotting (`evaluation/confusion_matrix.py`)
Generates an image of the confusion matrix and saves it under `results/graphs/`.

#### Latency (`evaluation/latency.py`)
Measures:

- average inference latency per image
- FPS (frames per second)

This is key for Edge AI evaluation.

### 8. Edge Optimization

#### TFLite Conversion (`optimization/tflite_converter.py`)
Converts a SavedModel to a `.tflite` file.

#### Quantization (`optimization/quantization.py`)
Supports optional INT8 quantization with a representative dataset.

#### Pruning (`optimization/pruning.py`)
Provides an optional pruning wrapper if TensorFlow Model Optimization is installed.

### 9. Inference

#### TensorFlow Inference (`inference/predict.py`)
Loads a Keras model and runs a single image prediction.

#### TFLite Inference (`inference/tflite_inference.py`)
Loads a TFLite interpreter and runs the same image through the optimized edge model.

### 10. Orchestration (`main.py`)
Main execution flow:

1. ensure output directories exist
2. load and prepare CIFAR-10 data
3. train each model in `MODEL_NAMES`
4. save training accuracy plots
5. load best checkpoint and export SavedModel
6. evaluate each model on test data
7. measure latency and calculate FPS
8. collect model comparison data
9. write a Markdown table and JSON latency report
10. select the best model by accuracy
11. convert that model to `.tflite`
12. run example inference for TensorFlow and TFLite

This produces a complete research pipeline from training to edge deployment.

---

## What has been created

- A full end-to-end Edge AI research codebase
- Modular architecture with clear separation of concerns
- Three model implementations for comparison
- Evaluation and optimization pipeline designed for edge deployment
- Result artifacts saved in `results/`
- `README.md` and `requirements.txt` for reproduction
- `PROJECT_DOCUMENTATION.md` describing the implementation

---

## Notes

- The current pipeline downloads CIFAR-10 at runtime, so `data/raw/` is not populated yet.
- To run the pipeline:

```bash
cd EdgeVisionNet
python main.py
```

- To enable quantization, update `TFLITE_QUANTIZE = True` in `utils/config.py`.
