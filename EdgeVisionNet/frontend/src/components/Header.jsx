import React from 'react';
import { motion } from 'framer-motion';
import { Zap } from 'lucide-react';

export const Header = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.3,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: -20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8, ease: 'easeOut' },
    },
  };

  return (
    <motion.div
      className="text-center mb-12 relative z-10"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div
        className="flex items-center justify-center gap-3 mb-4"
        variants={itemVariants}
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
        >
          <Zap className="w-8 h-8 text-yellow-400" />
        </motion.div>
        <h1 className="text-5xl font-bold bg-gradient-to-r from-yellow-400 to-yellow-600 bg-clip-text text-transparent">
          EdgeVisionNet
        </h1>
        <motion.div
          animate={{ rotate: -360 }}
          transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
        >
          <Zap className="w-8 h-8 text-yellow-400" />
        </motion.div>
      </motion.div>

      <motion.p
        className="text-yellow-200 text-lg mb-2"
        variants={itemVariants}
      >
        Real-time AI Image Classification
      </motion.p>

      <motion.p
        className="text-gray-400 text-sm"
        variants={itemVariants}
      >
        Optimized Edge Neural Networks for CIFAR-10 Classification
      </motion.p>

      {/* Animated underline */}
      <motion.div
        className="h-1 bg-gradient-to-r from-yellow-400 via-yellow-500 to-yellow-400 mt-6 mx-auto rounded-full"
        initial={{ width: 0 }}
        animate={{ width: 300 }}
        transition={{ duration: 1, delay: 0.5 }}
      />
    </motion.div>
  );
};
