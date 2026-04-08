"""
Backend configuration settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Server config
HOST = os.getenv('BACKEND_HOST', '0.0.0.0')
PORT = int(os.getenv('BACKEND_PORT', 5000))
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Model config
MODEL_PATH = os.getenv('MODEL_PATH', '../results/models/edgevisionnet.tflite')
IMAGE_SIZE = int(os.getenv('IMAGE_SIZE', 224))
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 1))
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.1))

# Upload config
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# CORS config
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'localhost:3000,localhost:3001').split(',')

# Inference settings
INFERENCE_TIMEOUT = int(os.getenv('INFERENCE_TIMEOUT', 30))

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
