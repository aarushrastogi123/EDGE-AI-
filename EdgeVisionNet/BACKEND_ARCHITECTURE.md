# BACKEND ARCHITECTURE

## Overview

The EdgeVisionNet Backend is a Flask-based REST API that serves image classification predictions using TensorFlow Lite models. It's designed for high performance, low latency inference on edge devices.

---

## Architecture Components

### 1. **Flask Application Core** (`app.py`)

The main application file orchestrates:
- Model loading and initialization
- HTTP endpoints for predictions and information
- Error handling and logging
- CORS configuration for frontend communication

#### Key Functions:

**`load_model()`**
- Loads the TFLite model from disk at startup
- Uses TensorFlow Lite Interpreter for optimized inference
- Runs once on application start to avoid repeated loading overhead

**`preprocess_image(image_bytes)`**
- Converts uploaded image to PIL Image object
- Resizes to model input size (224x224)
- Normalizes pixel values to [0, 1]
- Adds batch dimension required for inference
- Error handling for corrupted/invalid images

**`predict(image_array)`**
- Executes inference using TFLite Interpreter
- Applies softmax if needed
- Extracts top-5 predictions with confidence scores
- Filters by confidence threshold
- Returns structured prediction data

### 2. **Configuration Management** (`config.py`)

Centralized settings using environment variables:

```python
BACKEND_HOST = '0.0.0.0'          # Listen on all interfaces
BACKEND_PORT = 5000               # Default Flask port
IMAGE_SIZE = 224                  # Model input resolution
BATCH_SIZE = 1                    # Single image per request
CONFIDENCE_THRESHOLD = 0.1        # Minimum prediction confidence
MAX_CONTENT_LENGTH = 16MB         # Max upload size
INFERENCE_TIMEOUT = 30            # Timeout for predictions
```

Use `.env` file to override defaults:
```bash
cp backend/.env.example backend/.env
# Edit .env with your settings
```

---

## API Endpoints

### 1. **POST /predict**
**Image Classification Endpoint**

**Request:**
```
POST /predict HTTP/1.1
Content-Type: multipart/form-data

[binary image data]
```

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "predictions": [
      {
        "label": "dog",
        "confidence": 0.92,
        "percentage": "92.00%"
      },
      {
        "label": "cat",
        "confidence": 0.065,
        "percentage": "6.50%"
      }
    ],
    "top_prediction": {
      "label": "dog",
      "confidence": 0.92,
      "percentage": "92.00%"
    },
    "model": "EdgeVisionNet-TFLite"
  },
  "timestamp": "2024-04-07T10:30:45.123Z"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Invalid image format"
}
```

---

### 2. **GET /health**
**Health Check Endpoint**

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-04-07T10:30:45.123Z",
  "model_loaded": true
}
```

Use this to verify backend is running before frontend initialization.

---

### 3. **GET /models**
**Model Information Endpoint**

**Response:**
```json
{
  "available_models": ["EdgeVisionNet-TFLite"],
  "current_model": "EdgeVisionNet-TFLite",
  "input_size": 224,
  "num_classes": 10,
  "classes": [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck"
  ]
}
```

---

### 4. **GET /info**
**API Information Endpoint**

**Response:**
```json
{
  "name": "EdgeVisionNet API",
  "version": "1.0.0",
  "description": "Real-time image classification using edge-optimized neural networks",
  "endpoints": {
    "/health": "Health check",
    "/predict": "Image classification (POST with image file)",
    "/models": "Get available models",
    "/info": "API information"
  }
}
```

---

## Data Flow

```
┌─────────────────────────────────────────────────────┐
│ 1. Frontend sends image via POST /predict         │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 2. Flask receives multipart/form-data request     │
│    - Validates image presence                     │
│    - Validates file type                          │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 3. Image Preprocessing                             │
│    - Convert bytes → PIL Image                     │
│    - Resize 224x224                                │
│    - Normalize [0, 1]                              │
│    - Add batch dimension                           │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 4. TFLite Inference                                 │
│    - Load preprocessed image into model            │
│    - Run interpreter.invoke()                      │
│    - Get output predictions                        │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 5. Post-processing                                 │
│    - Apply softmax if needed                       │
│    - Sort predictions by confidence                │
│    - Filter by threshold                           │
│    - Format for frontend                           │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 6. Return JSON response to frontend                │
│    - Status + predictions                          │
│    - Timestamp                                     │
│    - Model metadata                                │
└─────────────────────────────────────────────────────┘
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Steps

1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your settings (optional)
```

3. **Prepare Model**
- Ensure your TFLite model exists at the path specified in `config.py`
- Default: `../results/models/edgevisionnet.tflite`

4. **Run Backend**
```bash
python app.py
```

Backend runs on `http://localhost:5000` by default.

---

## Performance Considerations

### Inference Latency
- **TFLite Model**: ~50-200ms per image (varies by device)
- **Network**: ~100-500ms for upload (depends on image size)
- **Total**: ~150-700ms end-to-end

### Optimizations

1. **Single Interpreter Instance**
   - Loaded once on startup
   - Reused for all requests (thread-safe)
   - Reduces memory footprint

2. **Efficient Preprocessing**
   - NumPy for fast image manipulation
   - Single pass normalization
   - Minimal copying

3. **Model Optimization**
   - TFLite format (much smaller than full TF)
   - Quantization support (if enabled)
   - Single batch per request

### Scaling Strategies

For production deployment:

1. **Horizontal Scaling**
```bash
# Run multiple instances with load balancer
gunicorn -w 4 app:app  # 4 worker processes
```

2. **Queue-Based Processing** (for high throughput)
- Use Celery + Redis
- Batch inference
- Asynchronous response via webhooks

3. **GPU Acceleration**
- Use TFLite GPU delegate
- Significant speedup for larger models

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "No image provided" | Missing image in request | Ensure `image` field in form data |
| "Invalid image format" | Corrupted/unsupported format | Use JPEG, PNG, BMP, TIFF |
| "Model not loaded" | TFLite model missing/corrupted | Check `MODEL_PATH` in config |
| "Inference timeout" | Model too slow or stuck | Reduce image size or optimize model |

### Logging

Logs appear in console and can be configured:
```python
LOG_LEVEL = 'INFO'  # or DEBUG, WARNING, ERROR
```

Check logs for:
- Model loading status
- Prediction confidence scores
- Processing time metrics
- Error stack traces

---

## Security Considerations

1. **File Upload Validation**
   - Check MIME types
   - Validate file size (max 16MB)
   - Scan for malicious files

2. **CORS Configuration**
   - Whitelist allowed origins
   - Restrict to trusted domains
   - Default: `localhost:3000`

3. **Input Sanitization**
   - Image validation before inference
   - Error messages don't leak internals
   - Rate limiting (add via reverse proxy)

4. **Production Deployment**
   - Use `gunicorn` instead of Flask dev server
   - Run behind Nginx reverse proxy
   - Enable HTTPS/TLS
   - Add authentication if needed

---

## Monitoring & Debugging

### Health Monitoring
```bash
# Check backend status
curl http://localhost:5000/health
```

### Performance Metrics
Add to `app.py` for monitoring:
```python
import time
start = time.time()
pred = predict(image_array)
inference_time = time.time() - start
logger.info(f"Inference time: {inference_time}ms")
```

### Load Testing
```bash
# Using Apache Bench
ab -n 100 -c 10 -p image.bin http://localhost:5000/predict
```

---

## Deployment Options

### 1. **Local Development**
```bash
python app.py  # Uses Flask dev server
```

### 2. **Production (Single Machine)**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. **Docker**
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Deploy:
```bash
docker build -t edgevisionnet-backend .
docker run -p 5000:5000 edgevisionnet-backend
```

### 4. **Cloud Deployment** (Azure/AWS/GCP)
- Containerize with Docker
- Deploy to container service (Azure Container Instances, AWS ECS, etc.)
- Use managed databases if needed
- Enable auto-scaling

---

## Testing

### Manual Testing
```bash
# Using curl
curl -X POST -F "image=@test.jpg" http://localhost:5000/predict

# Using Python
import requests
files = {'image': open('test.jpg', 'rb')}
r = requests.post('http://localhost:5000/predict', files=files)
print(r.json())
```

---

## Future Enhancements

1. **Batch Prediction** - Process multiple images per request
2. **Model Switching** - Load different models dynamically
3. **Caching** - Cache predictions for identical images
4. **Metrics** - Prometheus metrics for monitoring
5. **Async Processing** - Queue-based prediction with Celery
6. **GPU Support** - TFLite GPU delegate for faster inference
7. **Authentication** - API key validation
8. **Rate Limiting** - Prevent abuse

---

## Support & Troubleshooting

**Backend not starting?**
- Check Python version (3.8+)
- Verify all dependencies installed
- Check logs for model loading errors

**Slow inference?**
- Profile with `cProfile`
- Check CPU usage
- Consider quantization or pruning

**CORS errors?**
- Update `CORS_ORIGINS` in config
- Ensure frontend URL matches

**Connection refused?**
- Verify backend running on correct port
- Check firewall settings
- Ensure frontend API URL is correct

