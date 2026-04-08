import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AnimatedBackground } from './components/AnimatedBackground';
import { Header } from './components/Header';
import { ImageUpload } from './components/ImageUpload';
import { PredictionDisplay } from './components/PredictionDisplay';
import { predictImage } from './services/api';

function App() {
  const [predictions, setPredictions] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageUpload = async (file) => {
    setIsLoading(true);
    setError(null);
    setPredictions(null);

    try {
      const result = await predictImage(file);
      if (result.success) {
        setPredictions(result.data);
      } else {
        setError(result.error || 'Prediction failed');
      }
    } catch (err) {
      setError(
        err.response?.data?.error ||
        err.message ||
        'Failed to get prediction. Make sure the backend is running.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const pageVariants = {
    initial: { opacity: 0 },
    animate: { opacity: 1, transition: { duration: 0.8 } },
  };

  return (
    <div className="relative w-full min-h-screen bg-black overflow-hidden">
      {/* Animated background */}
      <AnimatedBackground />

      {/* Main content */}
      <motion.div
        className="relative z-20 min-h-screen flex flex-col items-center justify-center px-4 py-8"
        variants={pageVariants}
        initial="initial"
        animate="animate"
      >
        {/* Container */}
        <motion.div
          className="max-w-2xl w-full"
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          {/* Header Section */}
          <Header />

          {/* Main Content Area */}
          <div className="grid grid-cols-1 gap-8 items-center justify-items-center mt-12">
            {/* Image Upload */}
            <ImageUpload onImageUpload={handleImageUpload} isLoading={isLoading} />

            {/* Vertical divider with animation */}
            <AnimatePresence>
              {(predictions || error) && (
                <motion.div
                  className="w-20 h-1 bg-gradient-to-r from-transparent via-yellow-400 to-transparent"
                  initial={{ scaleX: 0 }}
                  animate={{ scaleX: 1 }}
                  exit={{ scaleX: 0 }}
                  transition={{ duration: 0.5 }}
                />
              )}
            </AnimatePresence>

            {/* Predictions Display */}
            <AnimatePresence>
              {(predictions || error || isLoading) && (
                <PredictionDisplay
                  predictions={predictions}
                  isLoading={isLoading}
                  error={error}
                />
              )}
            </AnimatePresence>
          </div>

          {/* Footer Info */}
          <motion.div
            className="mt-16 text-center text-gray-500 text-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
          >
            <p>Powered by EdgeVisionNet • Real-time AI Classification</p>
            <p className="mt-2">Supports CIFAR-10 image classification</p>
          </motion.div>
        </motion.div>
      </motion.div>

      {/* Corner decorations */}
      <motion.div
        className="fixed top-0 left-0 w-32 h-32 border-l-2 border-t-2 border-yellow-400/30 pointer-events-none"
        animate={{ opacity: [0.3, 0.6, 0.3] }}
        transition={{ duration: 3, repeat: Infinity }}
      />
      <motion.div
        className="fixed bottom-0 right-0 w-32 h-32 border-r-2 border-b-2 border-yellow-400/30 pointer-events-none"
        animate={{ opacity: [0.3, 0.6, 0.3] }}
        transition={{ duration: 3, repeat: Infinity, delay: 1.5 }}
      />
    </div>
  );
}

export default App;
