# FRONTEND-BACKEND INTEGRATION GUIDE

## System Overview

EdgeVisionNet is a full-stack application with clear separation of concerns:

```
┌──────────────────────────────────────────────────────────┐
│                     End User                             │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│         React Frontend (Port 3000)                       │
│  ┌────────────────────────────────────────────────────┐  │
│  │  - Upload Image                                    │  │
│  │  - Send via Axios API call                         │  │
│  │  - Display Results with Framer Motion              │  │
│  │  - Black + Golden Theme                            │  │
│  │  - Animated Background                             │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────┬───────────────────────────────────────┘
                   │
      HTTP POST /predict (JSON response)
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│         Flask Backend (Port 5000)                        │
│  ┌────────────────────────────────────────────────────┐  │
│  │  - Receive Image                                   │  │
│  │  - Preprocess (Resize, Normalize)                  │  │
│  │  - Load TFLite Model                               │  │
│  │  - Run Inference                                   │  │
│  │  - Return Predictions                              │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│         TensorFlow Lite Model                            │
│  - Optimized EdgeVisionNet                              │
│  - CIFAR-10 Classification                              │
│  - 224x224 Input Size                                   │
│  - 10 Output Classes                                    │
└──────────────────────────────────────────────────────────┘
```

---

## Communication Protocol

### Request-Response Cycle

#### 1. Frontend Initiates Request

**File:** `frontend/src/services/api.js`
```javascript
export const predictImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);

  const response = await api.post('/predict', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};
```

**What Happens:**
1. User selects image file
2. Image wrapped in `FormData` object
3. HTTP POST request sent with Content-Type `multipart/form-data`
4. Backend will receive file in `request.files['image']`

---

#### 2. Backend Receives & Processes

**File:** `backend/app.py`
```python
@app.route('/predict', methods=['POST'])
def predict_image():
    # Extract image from request
    file = request.files['image']
    image_bytes = file.read()
    
    # Preprocess
    image_array = preprocess_image(image_bytes)
    
    # Predict
    result = predict(image_array)
    
    # Return JSON
    return jsonify({
        'success': True,
        'data': result,
        'timestamp': datetime.now().isoformat()
    })
```

**Processing Steps:**
1. Extract binary image data from `request.files`
2. Validate file type (JPG, PNG, etc.)
3. Convert to PIL Image
4. Resize to 224x224
5. Normalize pixel values [0, 1]
6. Add batch dimension
7. Load into TFLite Interpreter
8. Run inference
9. Extract predictions and format response

---

#### 3. Frontend Receives Response

**File:** `frontend/src/App.jsx`
```jsx
const handleImageUpload = async (file) => {
  setIsLoading(true);
  setError(null);
  
  try {
    const result = await predictImage(file);
    
    if (result.success) {
      setPredictions(result.data);  // Store predictions
    }
  } catch (err) {
    setError(err.message);  // Handle errors
  } finally {
    setIsLoading(false);  // Update loading state
  }
};
```

**What Happens:**
1. Response automatically parsed from JSON
2. Store predictions in `state`
3. Handle errors gracefully
4. Update loading indicator
5. Components re-render showing results

---

## Detailed Communication Examples

### Example 1: Successful Classification

**Frontend Request:**
```
POST /predict HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data; boundary=----...

------WebKitFormBoundary...
Content-Disposition: form-data; name="image"; filename="dog.jpg"
Content-Type: image/jpeg

[binary image data - 50KB]
------WebKitFormBoundary...--
```

**Backend Processing:**
```
1. Receive 50KB JPEG image
2. Convert bytes → PIL Image (JPEG decoded)
3. Resize 256x256 → 224x224
4. Convert to RGB if needed
5. NumPy array: shape (224, 224, 3)
6. Normalize: divide by 255.0 → [0, 1] range
7. Expand dims: (1, 224, 224, 3) [batch size = 1]
8. Load into TFLite Interpreter
9. Run inference: interpreter.invoke()
10. Get raw output: shape (1, 10) [batch, classes]
11. Apply softmax if needed
12. Extract top predictions
```

**Backend Response:**
```json
{
  "success": true,
  "data": {
    "predictions": [
      {
        "label": "dog",
        "confidence": 0.923,
        "percentage": "92.30%"
      },
      {
        "label": "cat",
        "confidence": 0.065,
        "percentage": "6.50%"
      }
    ],
    "top_prediction": {
      "label": "dog",
      "confidence": 0.923,
      "percentage": "92.30%"
    },
    "model": "EdgeVisionNet-TFLite"
  },
  "timestamp": "2024-04-07T10:30:45.123Z"
}
```

**Frontend Display:**
```
┌─────────────────────────────────────────┐
│ ✓ TOP PREDICTION                        │
│                                         │
│ DOG                                     │
│ Confidence: 92.30%                      │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │████████████████████░░░░ 92.30%      │ │ (animated bar)
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

### Example 2: Error Handling

**Backend Error:** Image not provided
```json
{
  "success": false,
  "error": "No image provided"
}
```

**Frontend Display:**
```
┌────────────────────────────┐
│ ⚠ Error                   │
│                            │
│ No image provided          │
└────────────────────────────┘
```

---

### Example 3: Network Error (Backend Down)

**Frontend:**
```javascript
try {
  const response = await predictImage(file);
} catch (error) {
  // error.response is undefined
  // error.message: "Network Error"
  
  setError("Failed to get prediction. Make sure the backend is running.");
}
```

**Frontend Display:**
```
┌────────────────────────────────────────────────────┐
│ ⚠ Error                                            │
│                                                    │
│ Failed to get prediction. Make sure the backend    │
│ is running.                                        │
└────────────────────────────────────────────────────┘
```

---

## Environment Configuration

### Frontend Setup

**File:** `frontend/.env`
```
VITE_API_URL=http://localhost:5000
```

At build time, Vite processes this:
```javascript
// frontend/src/services/api.js
const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:5000';
```

---

### Backend Setup

**File:** `backend/.env`
```
BACKEND_HOST=0.0.0.0
BACKEND_PORT=5000
MODEL_PATH=../results/models/edgevisionnet.tflite
IMAGE_SIZE=224
CORS_ORIGINS=localhost:3000,localhost:3001,127.0.0.1:3000
```

Backend reads at startup:
```python
from config import HOST, PORT, CORS_ORIGINS
app.run(host=HOST, port=PORT)
```

---

## Running the Full Stack

### Step 1: Start Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Output:**
```
INFO:__main__:Loading model from ../results/models/edgevisionnet.tflite
INFO:__main__:Model loaded successfully
INFO:__main__:Starting EdgeVisionNet Backend API on http://localhost:5000
```

**Check Health:**
```bash
curl http://localhost:5000/health
# {"status": "healthy", "model_loaded": true, ...}
```

---

### Step 2: Start Frontend

**In new terminal:**
```bash
cd frontend
npm install
npm run dev
```

**Output:**
```
  VITE v4.4.9  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  press h to show help
```

**Open Browser:** `http://localhost:3000`

---

### Step 3: Test End-to-End

1. **Frontend loads** with animated background, black + golden theme
2. **Header animates in** with rotating lightning icons
3. **User uploads image** (JPG, PNG, etc.)
4. **Loading spinner** appears while backend processes
5. **Backend receives** image at `POST /predict`
6. **Backend processes:** preprocess → infer → format
7. **Backend returns** predictions in < 500ms
8. **Frontend receives** JSON response
9. **Predictions animate in** with confidence bars
10. **Top prediction** shows with glow effect

---

## Performance Metrics

### Timing Breakdown (Per Request)

| Component | Time | Details |
|-----------|------|---------|
| Frontend Upload | 50-200ms | File read + preview generation |
| Network Latency | 100-300ms | Upload to backend |
| Backend Preprocessing | 20-50ms | Resize, normalize, batch |
| TFLite Inference | 100-200ms | Model forward pass (CPU) |
| Backend Response Format | 10-20ms | JSON serialization |
| Network Response | 100-300ms | Response to frontend |
| Frontend Render | 50-100ms | React re-render + animations |
| **Total | 430-1170ms | ~700ms average |

### Optimization Tips

**Reduce Network Latency:**
- Deploy backend closer to user (CDN/regional server)
- Use HTTP/2 or HTTP/3
- Enable gzip compression

**Reduce Inference Time:**
- Use quantized TFLite model
- GPU acceleration (NNAPI on Android)
- Reduce image resolution

**Reduce Frontend Render Time:**
- Use React.memo for components
- Lazy load animations
- Minimize state updates

---

## API Contract

### Guaranteed Endpoints

Both frontend and backend must implement these exactly:

#### `/predict` POST Endpoint

**Request Format:**
```
Content-Type: multipart/form-data
Body:
  - image: File (image/jpeg, image/png, etc.)
```

**Response Format (Success):**
```json
{
  "success": true,
  "data": {
    "predictions": [
      { "label": "class", "confidence": 0.95, "percentage": "95.00%" }
    ],
    "top_prediction": { "label": "...", "confidence": 0.95, "percentage": "95.00%" },
    "model": "string"
  },
  "timestamp": "ISO-8601"
}
```

**Response Format (Error):**
```json
{
  "success": false,
  "error": "description"
}
```

---

## Testing the Integration

### Unit Tests (Backend)

```bash
# Test preprocessing
python -m pytest tests/test_preprocess.py

# Test inference
python -m pytest tests/test_inference.py
```

### Integration Tests (Full Flow)

```bash
# Using Python requests
import requests
from PIL import Image
from io import BytesIO

# Create test image
img = Image.new('RGB', (224, 224), color='red')
img_bytes = BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

# Send to backend
response = requests.post(
    'http://localhost:5000/predict',
    files={'image': img_bytes}
)

print(response.json())
```

### Frontend Component Tests

```javascript
// Using Vitest + React Testing Library
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

test('upload image shows predictions', async () => {
  render(<App />);
  
  const input = screen.getByRole('input');
  await userEvent.upload(input, 'test.jpg');
  
  // Wait for predictions to appear
  expect(await screen.findByText(/dog/i)).toBeInTheDocument();
});
```

---

## Deployment Architecture

### Local Development
```
Frontend (3000) ←→ Backend (5000)
Both on localhost
```

### Production Deployment
```
Vercel
  └─ frontend/dist
       ↓ (API calls)
Azure Container Instances / AWS ECS
  └─ Flask + Gunicorn
       ↓ (Model inference)
Models Storage (S3 / Azure Blob)
  └─ edgevisionnet.tflite
```

---

## Troubleshooting Integration

### Frontend Can't Connect to Backend

**Symptoms:** CORS error or connection refused

**Solutions:**
1. **Check backend is running:** `curl http://localhost:5000/health`
2. **Update CORS origins in backend config:**
   ```python
   CORS_ORIGINS=localhost:3000
   ```
3. **Check firewall:** Allow port 5000
4. **Verify API URL:** Check `frontend/.env` has correct backend URL

---

### Backend Can't Load Model

**Symptoms:** "Model not loaded" in health check

**Solutions:**
1. **Verify model path:** Check config.py MODEL_PATH
2. **Model exists:** `ls results/models/edgevisionnet.tflite`
3. **TensorFlow installed:** `pip install tensorflow`
4. **Model not corrupted:** Try with different model

---

### Predictions Are Wrong

**Debugging:**
1. **Check input preprocessing:** Add logging in `preprocess_image()`
2. **Verify model output:** Direct TFLite test
3. **Check model version:** Ensure correct model file
4. **Review training data:** Model expects CIFAR-10 data

---

### Slow Inference

1. **Profile backend:**
   ```python
   import cProfile
   cProfile.run('predict(image_array)')
   ```

2. **Optimize:**
   - Enable quantization
   - Use GPU acceleration
   - Reduce image resolution
   - Batch inference

---

## API Versioning Strategy

### Current Version: 1.0

Future versions can add new endpoints:

```
v1.0 (Current)
├─ POST /predict
├─ GET /health
├─ GET /models
└─ GET /info

v2.0 (Future)
├─ Previous endpoints
├─ POST /predict/batch (multiple images)
├─ GET /predict/history (recent predictions)
└─ POST /train (model retraining)
```

---

## Security Checklist

- [ ] CORS properly configured (not `*`)
- [ ] File upload size limited (16MB)
- [ ] File types validated (image/* only)
- [ ] No sensitive data in error messages
- [ ] Backend uses HTTPS in production
- [ ] Environment variables for secrets
- [ ] Rate limiting enabled
- [ ] Input validation on both sides
- [ ] CSRF tokens if needed
- [ ] Authentication/Authorization layer (future)

---

## Performance Monitoring

### Frontend Metrics
- Time to interactive (TTI)
- Animation frame rate (FPS)
- Bundle size

### Backend Metrics
- Requests per second (RPS)
- Average response time
- Inference latency
- Error rate

### Tools
- **Frontend:** Lighthouse, Web Vitals API
- **Backend:** Prometheus + Grafana, New Relic

---

## Cross-Browser Compatibility

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome/Edge | ✅ Latest | Full support |
| Firefox | ✅ Latest | Full support |
| Safari | ✅ Latest | Full support |
| Mobile Safari | ✅ iOS 14+ | Touch-optimized |
| Chrome Mobile | ✅ Android 11+ | Full support |

---

## Summary

The EdgeVisionNet full-stack application works through clear HTTP communication:

1. **Frontend (React)** → Collects user image → Sends via API
2. **Backend (Flask)** ← Receives image → Processes → Returns predictions
3. **Frontend (React)** ← Receives predictions → Displays with animations

Clean separation allows:
- Independent scaling
- Easy debugging
- Technology flexibility
- Team parallel development

