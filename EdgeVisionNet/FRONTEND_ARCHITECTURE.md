# FRONTEND ARCHITECTURE

## Overview

The EdgeVisionNet Frontend is a React-based web application featuring:
- **Black & Golden Theme** - Premium, modern aesthetic
- **Framer Motion Animations** - Smooth, top-level interactions
- **Animated Technology Background** - Live, dynamic visual effects
- **Real-time Image Classification** - Interactive prediction display
- **Responsive Design** - Works on desktop, tablet, mobile

---

## Design System

### Color Palette
```
Primary Background:    #000000 (Pure Black)
Accent Color:          #d4af37 (Golden)
Accent Light:          #f4d03f (Light Golden)
Text Primary:          #FFFFFF (White)
Text Secondary:        #A0AEC0 (Gray)
Border/Divider:        rgba(212, 175, 55, 0.5) (Golden 50%)
Success:               #48BB78 (Green)
Error:                 #F56565 (Red)
```

### Typography
```
Heading (H1):          5xl, Bold, Gradient Golden
Heading (H2):          3xl, Bold, Golden
Body Text:             base, Regular, Gray
Caption:               sm, Regular, Gray
```

---

## Architecture Components

### 1. **App Component** (`src/App.jsx`)

Main orchestrator managing:
- State for predictions, loading, and errors
- Image upload handling
- API communication with backend
- Layout composition

**State Management:**
```jsx
const [predictions, setPredictions] = useState(null);
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState(null);
```

**Flow:**
1. User uploads image
2. `handleImageUpload()` called
3. `predictImage()` API call sent to backend
4. Response stored in `predictions`
5. Components re-render with new data

---

### 2. **Animated Background** (`src/components/AnimatedBackground.jsx`)

Creates immersive tech-vibes atmosphere with:

#### Features:
- **Gradient Base** - Black to dark slate gradient
- **Golden Radial Glow** - Pulsing golden light at center
- **Floating Particles** - 20 golden particles with random trajectories
- **Grid Pattern** - Subtle SVG grid overlay
- **Animated Tech Lines** - Horizontal and vertical lines with animation

#### Animation Details:

**Radial Glow Pulse:**
```jsx
animate={{ opacity: [0.1, 0.3, 0.1] }}
transition={{ duration: 6, repeat: Infinity }}
```
- Smooth pulsing effect
- Creates living background feeling

**Particle Movement:**
```jsx
animate={{
  y: [0, -window.innerHeight],  // Move upward
  opacity: [0, 1, 0],            // Fade in and out
  x: particle.xOffset            // Slight horizontal drift
}}
transition={{
  duration: particle.duration,   // 10-30 seconds
  repeat: Infinity,
  ease: 'linear'
}}
```

**SVG Grid:**
- Repeating pattern at 50px intervals
- Very low opacity (5%) for subtle effect
- Reinforces tech aesthetic

**Tech Lines:**
- Horizontal and vertical lines
- Animated dash offset for flow effect
- Golden color with 30% opacity

---

### 3. **Header Component** (`src/components/Header.jsx`)

Premium branding with animations

#### Features:
- **Rotating Icons** - Lightning bolts rotating in/out (opposite directions)
- **Gradient Title** - "EdgeVisionNet" with golden gradient
- **Staggered Animations** - Title, subtitle, underline appear sequentially
- **Golden Underline** - Animates in from width 0 to 300px

#### Animation Sequence:
1. **Delay 0ms** - Lightning icons rotate
2. **Delay 300ms** - Title with gradient appears
3. **Delay 600ms** - Subtitle slides in
4. **Delay 500ms** - Golden underline animates

---

### 4. **Image Upload Component** (`src/components/ImageUpload.jsx`)

Interactive upload interface with rich animations

#### Features:
- **Upload Area**
  - Dashed golden border
  - Hover effect (scale + glow)
  - Drag-and-drop support
  - Click to select

- **Upload Icon**
  - Bob animation (up-down motion)
  - Changes text based on state

- **Image Preview**
  - Fades in smoothly
  - Golden border with glow
  - Dark overlay on hover
  - Loading spinner overlay during inference

- **Loading Indicator**
  - Rotating spinner
  - "Analyzing image..." text
  - Semi-transparent dark background

#### Key Animations:

**Bob Effect on Icon:**
```jsx
animate={{ y: [0, -10, 0] }}
transition={{ duration: 3, repeat: Infinity }}
```

**Image Preview Fade-in:**
```jsx
initial={{ opacity: 0, y: 10 }}
animate={{ opacity: 1, y: 0 }}
transition={{ duration: 0.4 }}
```

**Confidence Bar:**
```jsx
initial={{ scaleX: 0 }}
animate={{ scaleX: ture }}
transition={{ duration: 0.8, delay: 0.3 }}
```

---

### 5. **Prediction Display Component** (`src/components/PredictionDisplay.jsx`)

Shows classification results with animations

#### Features:

**Top Prediction Card:**
- Green checkmark icon
- Prediction label in large text
- Confidence percentage
- Animated confidence bar
- Gradient background with hover glow

**Other Predictions:**
- Top 5 predictions displayed
- Individual confidence bars
- Hover effect (slight slide right)
- Staggered appearance

#### Animations:

**Card Reveal:**
```jsx
initial={{ opacity: 0, scale: 0.9 }}
animate={{ opacity: 1, scale: 1 }}
```

**Confidence Bars:**
```jsx
// Bar container
initial={{ scaleX: 0 }}
animate={{ scaleX: 1 }}

// Bar fill
initial={{ scaleX: 0 }}
animate={{ scaleX: confidence }}
```

**Percentage Number Pulse:**
```jsx
animate={{ 
  scale: [1, 1.1, 1],
  rotate: [0, 5, 0]
}}
transition={{ duration: 2, repeat: Infinity }}
```

---

### 6. **API Service** (`src/services/api.js`)

Backend communication layer using Axios

#### Key Functions:

**`predictImage(imageFile)`**
```javascript
POST /predict
Content-Type: multipart/form-data
Body: { image: File }

Returns: {
  success: boolean,
  data: {
    predictions: Array,
    top_prediction: Object,
    model: string
  },
  timestamp: ISO string
}
```

**`getModels()`**
```javascript
GET /models
Returns: Model metadata and available classes
```

**`getHealth()`**
```javascript
GET /health
Returns: Backend health status
```

#### Error Handling:
- 404 errors → Connection refused message
- 500 errors → Server error
- Network errors → Descriptive user messages

---

## Styling

### Tailwind CSS Configuration

**Custom Theme (`tailwind.config.js`):**
```javascript
{
  colors: {
    'golden': '#d4af37'
  }
}
```

**Utility Classes Used:**
- `bg-black`, `bg-gradient-to-br`, `from-yellow-400`
- `border-yellow-400`, `text-yellow-300`
- `hover:scale-105`, `hover:border-yellow-300`
- `shadow-lg shadow-yellow-400/20` (glow effect)

### Global Styles (`src/index.css`)

```css
/* Custom animations */
@keyframes glow {
  0%, 100% { text-shadow: 0 0 10px rgba(212, 175, 55, 0.5); }
  50% { text-shadow: 0 0 20px rgba(212, 175, 55, 0.8); }
}

/* Scrollbar styling */
::-webkit-scrollbar { /* Golden scrollbar */ }
```

---

## Data Flow

```
┌────────────────────────────┐
│ 1. User selects image      │
│    via click/drag-drop     │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│ 2. ImageUpload component   │
│    - Create preview        │
│    - Show loading spinner  │
│    - Call onImageUpload()  │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│ 3. App.handleImageUpload() │
│    - Set isLoading = true  │
│    - Call predictImage()   │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│ 4. api.predictImage()      │
│    - Create FormData       │
│    - POST to /predict      │
└─────────────┬──────────────┘
              │
              ▼ (Network Request)
┌────────────────────────────┐
│ 5. Backend processes       │
│    - Preprocess image      │
│    - Run inference         │
│    - Return predictions    │
└─────────────┬──────────────┘
              │
              ▼ (Response)
┌────────────────────────────┐
│ 6. App receives response   │
│    - Set predictions       │
│    - Set isLoading = false │
│    - Clear errors          │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│ 7. Components re-render    │
│    - Show prediction card  │
│    - Animate results       │
│    - Display confidence    │
└────────────────────────────┘
```

---

## Component Hierarchy

```
<App>
├── <AnimatedBackground>        # Tech vibes background
├── <div className="z-20">      # Main content overlay
│   └── <motion.div>            # Page fade-in animation
│       ├── <Header />          # Branding + title
│       ├── <div className="grid">
│       │   ├── <ImageUpload /> # Upload interface
│       │   ├── <divider>       # Animated line (conditional)
│       │   └── <PredictionDisplay /> # Results (conditional)
│       └── <Footer>            # Info text
└── <motion.div>                # Corner decorations (TL, BR)
```

---

## Installation & Setup

### Prerequisites
- Node.js 16+ and npm/yarn

### Steps

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with backend URL
VITE_API_URL=http://localhost:5000
```

3. **Run Development Server**
```bash
npm run dev
```

Frontend runs on `http://localhost:3000`

4. **Build for Production**
```bash
npm run build
# Output: frontend/dist/
```

---

## Animation Library: Framer Motion

### Key Concepts Used

**`<motion.*>` Components**
- Replace standard HTML elements with animated versions
- Automatically handles animation lifecycle

**Variants**
- Reusable animation definitions
- Named states: `hidden`, `visible`, etc.
```jsx
const variants = {
  hidden: { opacity: 0, y: -20 },
  visible: { opacity: 1, y: 0 }
}

<motion.div variants={variants} initial="hidden" animate="visible" />
```

**Transitions**
- Control animation timing and easing
```jsx
transition={{
  duration: 0.8,           // seconds
  delay: 0.3,              // delay before start
  ease: 'easeOut',         // easing function
  repeat: Infinity,        // loop infinitely
  repeatType: 'reverse'    // reverse direction
}}
```

**Stagger Children**
- Delay animation of child elements
```jsx
variants={{
  parent: {
    staggerChildren: 0.2  // 200ms between children
  }
}}
```

**AnimatePresence**
- Handle component enter/exit animations
```jsx
<AnimatePresence>
  {predictions && <PredictionDisplay />}
</AnimatePresence>
```

---

## Performance Optimization

### 1. **Lazy Background Animations**
- Only 20 particles (not 100+)
- GPU-accelerated transforms (`y`, `opacity`)
- No layout shifts

### 2. **Component Memoization** (Future)
```jsx
export const Header = memo(HeaderComponent);
```

### 3. **Image Optimization**
- Frontend sends compressed images
- Backend handles resizing

### 4. **Bundle Optimization**
- Use `npm run build` for tree-shaking
- Production build: ~100KB (gzipped)

---

## Responsive Design

### Breakpoints (Tailwind)
```
Mobile:   < 640px      (sm)
Tablet:   640-1024px   (md)
Desktop:  > 1024px     (lg)
```

### Responsive Classes Used:
- `max-w-2xl` - Constrains content width
- `px-4` - Padding on small screens
- `grid grid-cols-1` - Single column on mobile
- Text scaling: `text-2xl sm:text-3xl lg:text-5xl`

---

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: iOS 14+, Android 11+

---

## Testing

### Manual Testing Checklist

- [ ] Image upload works (click and drag-drop)
- [ ] Loading spinner appears during inference
- [ ] Predictions display with animations
- [ ] Confidence bars animate in
- [ ] Top prediction card has glow effect
- [ ] Background particles move smoothly
- [ ] App is responsive on mobile
- [ ] Errors display gracefully

### Browser Developer Tools

**Check Performance:**
```javascript
// In DevTools console
performance.measure('prediction');
performance.getEntriesByType('measure');
```

---

## Future Enhancements

1. **Themes** - Dark/Light mode toggle
2. **Image History** - Recent predictions gallery
3. **Batch Upload** - Multiple images at once
4. **Real-time Webcam** - Live camera feed
5. **Advanced Filters** - Image preprocessing options
6. **Model Selection** - Switch between models
7. **Analytics** - Prediction statistics
8. **Accessibility** - ARIA labels, keyboard navigation

---

## Deployment

### Production Build
```bash
npm run build
# Creates: frontend/dist/
```

### Static Hosting Options

**1. Vercel** (Recommended)
```bash
npm i -g vercel
vercel
```

**2. Netlify**
```bash
npm i -g netlify-cli
netlify deploy --prod --dir=dist
```

**3. AWS S3 + CloudFront**
```bash
aws s3 cp dist/ s3://my-bucket/ --recursive
```

**4. Docker**
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS errors | Update backend `CORS_ORIGINS` |
| Backend connection refused | Ensure backend running on :5000 |
| Animations laggy | Reduce particle count, check GPU |
| Images not uploading | Check `MAX_FILE_SIZE` in backend |
| Predictions not showing | Check browser console for API errors |

---

## Support & Resources

- **Framer Motion Docs**: https://www.framer.com/motion/
- **Tailwind CSS**: https://tailwindcss.com/
- **React Docs**: https://react.dev/
- **Vite**: https://vitejs.dev/

