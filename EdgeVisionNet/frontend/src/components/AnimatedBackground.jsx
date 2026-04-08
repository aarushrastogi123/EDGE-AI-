import React from 'react';
import { motion } from 'framer-motion';

export const AnimatedBackground = () => {
  const particles = Array.from({ length: 20 }).map((_, i) => ({
    id: i,
    size: Math.random() * 5 + 2,
    duration: Math.random() * 20 + 10,
    delay: Math.random() * 5,
    xOffset: Math.random() * 100 - 50,
  }));

  return (
    <div className="fixed inset-0 overflow-hidden bg-black pointer-events-none">
      {/* Gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-black via-black to-slate-900" />

      {/* Golden gradient overlay */}
      <motion.div
        className="absolute inset-0 opacity-20"
        style={{
          background: 'radial-gradient(circle at 50% 50%, #d4af37 0%, transparent 70%)',
        }}
        animate={{
          opacity: [0.1, 0.3, 0.1],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
        }}
      />

      {/* Animated particles */}
      {particles.map((particle) => (
        <motion.div
          key={particle.id}
          className="absolute rounded-full bg-yellow-500"
          style={{
            width: particle.size,
            height: particle.size,
            left: `${Math.random() * 100}%`,
            filter: 'blur(1px)',
          }}
          animate={{
            y: [0, -window.innerHeight],
            opacity: [0, 1, 0],
            x: particle.xOffset,
          }}
          transition={{
            duration: particle.duration,
            delay: particle.delay,
            repeat: Infinity,
            ease: 'linear',
          }}
        />
      ))}

      {/* Grid pattern overlay */}
      <div className="absolute inset-0 opacity-5">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
              <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#d4af37" strokeWidth="0.5" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      {/* Animated tech lines */}
      <motion.svg
        className="absolute inset-0 w-full h-full"
        viewBox="0 0 1000 1000"
        preserveAspectRatio="none"
      >
        <motion.line
          x1="0"
          y1="500"
          x2="1000"
          y2="500"
          stroke="#d4af37"
          strokeWidth="1"
          opacity="0.3"
          animate={{ strokeDashoffset: 1000 }}
          transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
        />
        <motion.line
          x1="500"
          y1="0"
          x2="500"
          y2="1000"
          stroke="#d4af37"
          strokeWidth="1"
          opacity="0.3"
          animate={{ strokeDashoffset: 1000 }}
          transition={{ duration: 20, repeat: Infinity, ease: 'linear', delay: 2 }}
        />
      </motion.svg>
    </div>
  );
};
