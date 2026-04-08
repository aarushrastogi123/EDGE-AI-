"""
EdgeVisionNet Backend API
Serves predictions using TensorFlow Lite models with Flask
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
UPLOAD_FOLDER = 'uploads'
MODEL_PATH = '../results/models/edgevisionnet.tflite'  # or your model path
IMAGE_SIZE = 224
CONFIDENCE_THRESHOLD = 0.1

# CIFAR-10 class labels
CIFAR10_LABELS = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global interpreter (loaded once)
interpreter = None


def load_model():
    """Load TensorFlow Lite model"""
    global interpreter
    try:
        logger.info(f"Loading model from {MODEL_PATH}")
        interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
        interpreter.allocate_tensors()
        logger.info("Model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False


def preprocess_image(image_bytes):
    """
    Preprocess image for model inference
    Args:
        image_bytes: Image file bytes
    Returns:
        preprocessed numpy array
    """
    try:
        # Load image
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Resize to model input size
        image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
        
        # Convert to numpy array and normalize
        image_array = np.array(image, dtype=np.float32)
        image_array = image_array / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        raise


def predict(image_array):
    """
    Run inference on preprocessed image
    Args:
        image_array: Preprocessed numpy array with batch dimension
    Returns:
        predictions dict with class labels and confidence scores
    """
    try:
        # Get input and output details
        input_details = interpreter.get_input_details() # type: ignore
        output_details = interpreter.get_output_details()
        
        # Set input tensor
        interpreter.set_tensor(input_details[0]['index'], image_array)
        
        # Run inference
        interpreter.invoke()
        
        # Get output
        output_data = interpreter.get_tensor(output_details[0]['index'])
        predictions = output_data[0]  # Remove batch dimension
        
        # Apply softmax if not already applied
        if np.max(predictions) > 1.0:
            predictions = tf.nn.softmax(predictions).numpy()
        
        # Get top predictions
        top_indices = np.argsort(predictions)[::-1][:5]  # Top 5
        
        results = []
        for idx in top_indices:
            confidence = float(predictions[idx])
            if confidence >= CONFIDENCE_THRESHOLD:
                results.append({
                    'label': CIFAR10_LABELS[int(idx)],
                    'confidence': confidence,
                    'percentage': f"{confidence * 100:.2f}%"
                })
        
        return {
            'predictions': results,
            'top_prediction': results[0] if results else None,
            'model': 'EdgeVisionNet-TFLite'
        }
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': interpreter is not None
    }), 200


@app.route('/predict', methods=['POST'])
def predict_image():
    """
    Main prediction endpoint
    Expects: multipart/form-data with image file
    Returns: JSON with predictions
    """
    try:
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read image bytes
        image_bytes = file.read()
        
        # Preprocess image
        image_array = preprocess_image(image_bytes)
        
        # Run prediction
        result = predict(image_array)
        
        # Log prediction
        logger.info(f"Prediction: {result['top_prediction']['label']} ({result['top_prediction']['percentage']})")
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/models', methods=['GET'])
def get_models():
    """Get available models and their info"""
    return jsonify({
        'available_models': ['EdgeVisionNet-TFLite'],
        'current_model': 'EdgeVisionNet-TFLite',
        'input_size': IMAGE_SIZE,
        'num_classes': len(CIFAR10_LABELS),
        'classes': CIFAR10_LABELS
    }), 200


@app.route('/info', methods=['GET'])
def get_info():
    """Get API information"""
    return jsonify({
        'name': 'EdgeVisionNet API',
        'version': '1.0.0',
        'description': 'Real-time image classification using edge-optimized neural networks',
        'endpoints': {
            '/health': 'Health check',
            '/predict': 'Image classification (POST with image file)',
            '/models': 'Get available models',
            '/info': 'API information'
        }
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Load model on startup
    if load_model():
        logger.info("Starting EdgeVisionNet Backend API on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        logger.error("Failed to load model. Server not starting.")
