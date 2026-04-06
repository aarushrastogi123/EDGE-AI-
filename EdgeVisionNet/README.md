# EdgeVisionNet

EdgeVisionNet is a modular research-grade Edge AI pipeline for CIFAR-10 image classification. It includes training, evaluation, model comparison, edge optimization, and inference using both TensorFlow and TensorFlow Lite.

## Project Structure

- `data/`
  - `raw/`
  - `processed/`
- `models/`
  - `mobilenet.py`
  - `efficientnet.py`
  - `edgevisionnet.py`
- `training/`
  - `train.py`
  - `augment.py`
  - `callbacks.py`
- `evaluation/`
  - `metrics.py`
  - `confusion_matrix.py`
  - `latency.py`
- `optimization/`
  - `quantization.py`
  - `pruning.py`
  - `tflite_converter.py`
- `inference/`
  - `predict.py`
  - `tflite_inference.py`
- `utils/`
  - `config.py`
  - `logger.py`
- `results/`
  - `graphs/`
  - `reports/`
  - `models/`
- `main.py`

## Features

- CIFAR-10 dataset loading and preprocessing
- Resize to `224x224`, normalization, and train/validation/test splitting
- MobileNetV2, EfficientNet-B0, and custom EdgeVisionNet model architectures
- Data augmentation: rotation, horizontal flip, zoom
- Training loop with early stopping and checkpoint saving
- Metrics: accuracy, precision, recall, F1 score, confusion matrix
- Latency measurement and FPS reporting
- TensorFlow Lite conversion and optional quantization
- Inference using TensorFlow and TFLite
- Report generation in `results/reports`

## Installation

```bash
cd EdgeVisionNet
python -m pip install -r requirements.txt
```

If you want optional pruning support, install:

```bash
python -m pip install tensorflow-model-optimization
```

## Usage

Run the full pipeline:

```bash
python main.py
```

Generated artifacts will be stored in `results/`:

- `results/graphs/`
- `results/reports/`
- `results/models/`

## Notes

- The project is designed to simulate a realistic Edge AI research workflow.
- Update hyperparameters in `utils/config.py` for batch size, epochs, learning rate, and model selection.
- Use `config.TFLITE_QUANTIZE = True` to enable TFLite quantization in `utils/config.py`.
