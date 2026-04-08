import React, { useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, Image as ImageIcon } from 'lucide-react';

export const ImageUpload = ({ onImageUpload, isLoading }) => {
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target?.result);
      };
      reader.readAsDataURL(file);

      // Call parent handler
      onImageUpload(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('image/')) {
      const event = { target: { files: [file] } };
      handleFileSelect(event);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0, scale: 0.9 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: { duration: 0.5, ease: 'easeOut' },
    },
  };

  const bobVariants = {
    animate: {
      y: [0, -10, 0],
      transition: {
        duration: 3,
        repeat: Infinity,
        ease: 'easeInOut',
      },
    },
  };

  return (
    <motion.div
      className="w-full max-w-md"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div
        className="relative"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        {/* Upload area */}
        <motion.div
          className="border-2 border-dashed border-yellow-400 rounded-lg p-8 text-center cursor-pointer transition-all duration-300 hover:border-yellow-300 hover:bg-yellow-400/5 relative overflow-hidden group"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => fileInputRef.current?.click()}
        >
          {/* Background glow */}
          <div className="absolute inset-0 opacity-0 group-hover:opacity-10 bg-yellow-400 transition-opacity duration-300" />

          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            accept="image/*"
            className="hidden"
            disabled={isLoading}
          />

          <motion.div variants={bobVariants} animate="animate">
            <Upload className="w-12 h-12 text-yellow-400 mx-auto mb-3" />
          </motion.div>

          <p className="text-yellow-300 font-semibold mb-1">
            {isLoading ? 'Analyzing...' : 'Upload an image'}
          </p>
          <p className="text-gray-400 text-sm">
            Drag and drop or click to select
          </p>
        </motion.div>

        {/* Preview */}
        {preview && (
          <motion.div
            className="mt-6 relative"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <div className="relative rounded-lg overflow-hidden border border-yellow-400/50 shadow-lg shadow-yellow-400/20">
              <img
                src={preview}
                alt="Preview"
                className="w-full h-auto object-cover"
              />
              
              {/* Image overlay effect */}
              <motion.div
                className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"
                animate={{
                  opacity: [0.3, 0.1, 0.3],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                }}
              />

              {/* Loading indicator */}
              {isLoading && (
                <motion.div
                  className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <div className="flex flex-col items-center gap-3">
                    <motion.div
                      className="w-8 h-8 border-2 border-yellow-400 border-t-transparent rounded-full"
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                    />
                    <span className="text-yellow-400 text-sm font-semibold">
                      Analyzing image...
                    </span>
                  </div>
                </motion.div>
              )}
            </div>

            <motion.button
              className="mt-4 w-full py-2 px-4 bg-yellow-500 hover:bg-yellow-400 text-black font-bold rounded-lg transition-colors duration-300 disabled:opacity-50"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              disabled={isLoading}
              onClick={() => {
                setPreview(null);
                fileInputRef.current = null;
              }}
            >
              Clear Image
            </motion.button>
          </motion.div>
        )}
      </motion.div>
    </motion.div>
  );
};
