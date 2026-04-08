import React from 'react';
import { motion } from 'framer-motion';
import { Check, AlertCircle, TrendingUp } from 'lucide-react';

export const PredictionDisplay = ({ predictions, isLoading, error }) => {
  if (isLoading) {
    return (
      <motion.div
        className="w-full max-w-md"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center justify-center">
          <motion.div
            className="w-10 h-10 border-3 border-yellow-400 border-t-transparent rounded-full"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          />
        </div>
      </motion.div>
    );
  }

  if (error) {
    return (
      <motion.div
        className="w-full max-w-md"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <motion.div
          className="border border-red-500 bg-red-500/10 rounded-lg p-6 flex items-start gap-4"
          whileHover={{ scale: 1.02 }}
        >
          <AlertCircle className="w-6 h-6 text-red-400 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-red-400 font-semibold mb-1">Error</h3>
            <p className="text-red-300 text-sm">{error}</p>
          </div>
        </motion.div>
      </motion.div>
    );
  }

  if (!predictions) {
    return null;
  }

  const topPrediction = predictions.top_prediction;
  const allPredictions = predictions.predictions || [];

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.5, ease: 'easeOut' },
    },
  };

  return (
    <motion.div
      className="w-full max-w-md"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Top prediction card */}
      {topPrediction && (
        <motion.div
          className="bg-gradient-to-br from-yellow-500/20 to-yellow-600/10 border border-yellow-400/50 rounded-lg p-6 mb-6 relative overflow-hidden group"
          variants={itemVariants}
          whileHover={{ scale: 1.02 }}
        >
          {/* Background animation */}
          <motion.div
            className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
            animate={{
              background: ['radial-gradient(circle at 0% 0%, rgba(212, 175, 55, 0.1) 0%, transparent 50%)', 
                          'radial-gradient(circle at 100% 100%, rgba(212, 175, 55, 0.1) 0%, transparent 50%)'],
            }}
            transition={{ duration: 3, repeat: Infinity }}
          />

          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-3">
              <Check className="w-5 h-5 text-green-400" />
              <span className="text-gray-400 text-sm font-semibold">TOP PREDICTION</span>
            </div>

            <div className="flex items-end justify-between">
              <div>
                <h2 className="text-3xl font-bold text-yellow-300 capitalize mb-2">
                  {topPrediction.label}
                </h2>
                <p className="text-gray-400 text-sm">
                  Confidence: <span className="text-yellow-400 font-bold">{topPrediction.percentage}</span>
                </p>
              </div>

              <motion.div
                className="text-4xl font-bold text-yellow-400/30"
                animate={{ 
                  scale: [1, 1.1, 1],
                  rotate: [0, 5, 0],
                }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                {Math.round(topPrediction.confidence * 100)}%
              </motion.div>
            </div>

            {/* Confidence bar */}
            <motion.div
              className="mt-4 h-2 bg-black/50 rounded-full overflow-hidden"
              initial={{ scaleX: 0 }}
              animate={{ scaleX: 1 }}
              transition={{ duration: 0.8, delay: 0.3 }}
            >
              <motion.div
                className="h-full bg-gradient-to-r from-yellow-400 to-yellow-600 rounded-full"
                initial={{ scaleX: 0 }}
                animate={{ scaleX: topPrediction.confidence }}
                transition={{ duration: 1, delay: 0.5, ease: 'easeOut' }}
              />
            </motion.div>
          </div>
        </motion.div>
      )}

      {/* Other predictions */}
      {allPredictions.length > 1 && (
        <motion.div variants={itemVariants}>
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-5 h-5 text-yellow-400" />
            <h3 className="text-gray-400 font-semibold text-sm">OTHER PREDICTIONS</h3>
          </div>

          <div className="space-y-2">
            {allPredictions.slice(1).map((pred, index) => (
              <motion.div
                key={index}
                className="bg-black/40 border border-yellow-400/20 rounded-lg p-3 hover:border-yellow-400/40 transition-colors"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                whileHover={{ x: 5 }}
              >
                <div className="flex justify-between items-center mb-2">
                  <span className="text-yellow-200 font-semibold capitalize">
                    {pred.label}
                  </span>
                  <span className="text-yellow-400 text-sm">{pred.percentage}</span>
                </div>
                <motion.div
                  className="h-1 bg-black/50 rounded-full overflow-hidden"
                  initial={{ scaleX: 0 }}
                  animate={{ scaleX: 1 }}
                  transition={{ delay: 0.5 + index * 0.1 }}
                >
                  <motion.div
                    className="h-full bg-gradient-to-r from-yellow-500/60 to-yellow-600/40"
                    initial={{ scaleX: 0 }}
                    animate={{ scaleX: pred.confidence }}
                    transition={{ duration: 0.8, delay: 0.6 + index * 0.1 }}
                  />
                </motion.div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};
