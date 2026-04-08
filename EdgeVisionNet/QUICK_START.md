# QUICK START GUIDE

Get EdgeVisionNet up and running in 5 minutes!

---

## Prerequisites

- Python 3.8+
- Node.js 16+ with npm
- Your trained TFLite model at `results/models/edgevisionnet.tflite`

---

## Step 1: Backend Setup (2 mins)

### 1.1 Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 1.2 Configure Environment (Optional)
```bash
cp .env.example .env
# Edit .env if needed (default settings work fine)
```

### 1.3 Verify Model Path
Make sure your model exists at: `../results/models/edgevisionnet.tflite`

### 1.4 Start Backend
```bash
python app.py
```

You should see:
```
INFO:__main__:Loading model from ../results/models/edgevisionnet.tflite
INFO:__main__:Model loaded successfully
INFO:__main__:Starting EdgeVisionNet Backend API on http://localhost:5000
```

✅ **Backend running on http://localhost:5000**

---

## Step 2: Frontend Setup (2 mins)

### 2.1 Install Dependencies
**In a new terminal:**
```bash
cd frontend
npm install
```

### 2.2 Configure Environment (Optional)
```bash
cp .env.example .env
# Default API URL is http://localhost:5000 (perfect for local dev)
```

### 2.3 Start Frontend
```bash
npm run dev
```

You should see:
```
➜  Local:   http://localhost:3000/
➜  press h to show help
```

✅ **Frontend running on http://localhost:3000**

---

## Step 3: Test Locally (1 min)

### 3.1 Open Browser
Navigate to: **http://localhost:3000**

You should see:
- ⚡ **EdgeVisionNet** title with animated lightning bolts
- Black background with golden animated particles
- Upload area with dashed golden border

### 3.2 Upload an Image
1. Click the upload area or drag-drop an image
2. Supported formats: JPG, PNG, BMP, TIFF
3. Recommended size: 224x224 or larger (will be resized)

### 3.3 See Results
1. Loading spinner appears while backend processes
2. Predictions display with:
   - Top prediction (green checkmark)
   - Confidence percentage
   - Animated confidence bar
   - Other top-5 predictions

---

## Typical Workflow

```
Terminal 1 (Backend)         Terminal 2 (Frontend)    Browser
├─ cd backend                ├─ cd frontend           
├─ python app.py             ├─ npm run dev           
├─ Model loaded              ├─ Listening :3000       
└─ Awaiting requests         └─ Ready                 ← Open http://localhost:3000
                                                      ← Upload image
← POST /predict              
← Process image              
← Run inference              
└─ Return predictions        → Display results
```

---

## Structure

```
EdgeVisionNet/
├── backend/                    # Flask API
│   ├── app.py                 # Main application
│   ├── config.py              # Configuration
│   ├── requirements.txt        # Python dependencies
│   └── .env                   # Your local config
│
├── frontend/                   # React App
│   ├── src/
│   │   ├── App.jsx           # Main component
│   │   ├── components/       # Reusable components
│   │   └── services/         # API calls
│   ├── package.json          # JS dependencies
│   ├── vite.config.js        # Build config
│   └── .env                  # Your local config
│
├── results/
│   └── models/
│       └── edgevisionnet.tflite   # Your model (required)
│
└── Documentation files
    ├── BACKEND_ARCHITECTURE.md
    ├── FRONTEND_ARCHITECTURE.md
    └── FRONTEND_BACKEND_INTEGRATION.md
```

---

## Common Issues & Fixes

### Issue: "ModuleNotFoundError: No module named 'tensorflow'"

**Fix:**
```bash
pip install tensorflow
```

---

### Issue: "File not found: ../results/models/edgevisionnet.tflite"

**Fix:**
1. Verify model file exists:
   ```bash
   ls results/models/edgevisionnet.tflite
   ```

2. Update path in `backend/config.py`:
   ```python
   MODEL_PATH = 'path/to/your/model.tflite'
   ```

---

### Issue: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Fix:** Update backend `CORS_ORIGINS`:

**File:** `backend/.env`
```
CORS_ORIGINS=localhost:3000
```

Then restart backend.

---

### Issue: "Backend connection refused" on frontend

**Fix:**
1. Ensure backend is running: `curl http://localhost:5000/health`
2. Check backend port matches frontend config
3. Try: `http://127.0.0.1:5000` instead of `localhost:5000`

---

### Issue: Animations very slow/laggy

**Fix:**
- Close other apps
- Use Chrome (better performance)
- Reduce browser zoom
- Check GPU acceleration enabled in Chrome settings

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `h` | Show Vite help menu (frontend terminal) |
| `r` | Refresh app (frontend terminal) |
| `q` | Quit dev server (any terminal) |
| `Ctrl+C` | Force quit (any terminal) |

---

## What's Happening Behind the Scenes

```
User uploads image.jpg
  │
  ├─→ Frontend: Stores in state
  ├─→ Frontend: Creates FormData with image
  ├─→ Frontend: Shows loading spinner
  │
  └─→ POST /predict (with image as binary)
      │
      └─→ Backend: Receives image bytes
      ├─→ Backend: Convert JPEG → PIL Image
      ├─→ Backend: Resize to 224x224
      ├─→ Backend: Normalize pixels [0, 1]
      ├─→ Backend: Load into TFLite
      ├─→ Backend: Run inference (< 200ms)
      ├─→ Backend: Extract top predictions
      │
      └─→ Return JSON {predictions, confidence, ...}
          │
          ├─→ Frontend: Parse JSON
          ├─→ Frontend: Hide spinner
          ├─→ Frontend: Update state
          │
          └─→ React: Re-render
              ├─→ AnimatedBackground: Continues animating
              ├─→ Header: Already visible
              ├─→ ImageUpload: Shows preview
              │
              └─→ PredictionDisplay: Animate in
                  ├─→ Top prediction card slides in
                  ├─→ Confidence bar animates
                  └─→ Other predictions stagger in
```

---

## Next Steps

### For Development
1. **Modify theme:** Edit colors in `frontend/src/components/*`
2. **Change animations:** Modify `framer-motion` configs
3. **Add features:** New components in `frontend/src/components/`
4. **Customize backend:** Adjust model path, confidence threshold, etc.

### For Production
1. **Build frontend:**
   ```bash
   cd frontend
   npm run build
   # Creates: frontend/dist/
   ```

2. **Deploy frontend:** Vercel, Netlify, AWS S3, etc.

3. **Deploy backend:** Docker, AWS ECS, Azure Container Instances, etc.

See **FRONTEND_BACKEND_INTEGRATION.md** for deployment details.

### For Improvement
1. **Batch images:** Add batch processing endpoint
2. **Image history:** Save recent predictions
3. **Camera input:** Real-time webcam inference
4. **Model switching:** Load different models dynamically
5. **Analytics:** Track prediction statistics

---

## Documentation

Read these for deeper understanding:

- **[BACKEND_ARCHITECTURE.md](./BACKEND_ARCHITECTURE.md)** - API design, endpoints, data flow
- **[FRONTEND_ARCHITECTURE.md](./FRONTEND_ARCHITECTURE.md)** - React components, animations, styling
- **[FRONTEND_BACKEND_INTEGRATION.md](./FRONTEND_BACKEND_INTEGRATION.md)** - How they work together, deployment

---

## Performance Expectations

| Operation | Time |
|-----------|------|
| Page load (first time) | 2-3 seconds |
| Page load (cached) | < 1 second |
| Image upload | 0.1-0.2s |
| Network round-trip | 0.1-0.3s |
| Model inference | 0.1-0.2s |
| Results display | 0.05-0.1s |
| **Total** | **~0.4-0.7s** |

---

## Stopping Services

### Stop Frontend (Terminal 1)
```
Press Ctrl + C
```

### Stop Backend (Terminal 2)
```
Press Ctrl + C
```

---

## Advanced: Running Multiple Backends

For testing or distributed inference:

```bash
# Terminal 1
BACKEND_PORT=5000 python app.py

# Terminal 2
BACKEND_PORT=5001 python app.py

# Terminal 3 (Use from frontend)
VITE_API_URL=http://localhost:5000 npm run dev
```

---

## Help & Support

### Check Logs
- **Frontend:** Browser DevTools console (F12)
- **Backend:** Terminal output (stdout/stderr)

### Debug API Calls
```javascript
// In browser console
fetch('http://localhost:5000/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

### Test Backend Directly
```bash
# Health check
curl http://localhost:5000/health

# Models info
curl http://localhost:5000/models

# Predict with file
curl -F "image=@test.jpg" http://localhost:5000/predict
```

---

## Next: Production Deployment

After successful local testing, follow the deployment sections in:
- [BACKEND_ARCHITECTURE.md - Deployment Options](./BACKEND_ARCHITECTURE.md#deployment-options)
- [FRONTEND_ARCHITECTURE.md - Deployment](./FRONTEND_ARCHITECTURE.md#deployment)

---

**🎉 You're all set! Enjoy your AI-powered image classification app!**

