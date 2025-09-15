#!/usr/bin/env python3
"""Sample script to train a Kolam detection model."""

import sys
import os
import numpy as np
import tensorflow as tf
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)


def create_sample_model():
    """Create a sample Kolam detection model."""
    logger.info("Creating sample Kolam detection model")
    
    # Create a simple CNN model for Kolam pattern detection
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(224, 224, 3)),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(10, activation='softmax')  # 10 pattern classes
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def generate_sample_data():
    """Generate sample training data."""
    logger.info("Generating sample training data")
    
    # Generate random image data (in practice, you'd load real images)
    num_samples = 1000
    X = np.random.random((num_samples, 224, 224, 3)).astype(np.float32)
    y = np.random.randint(0, 10, num_samples)
    y = tf.keras.utils.to_categorical(y, 10)
    
    return X, y


def train_model():
    """Train the Kolam detection model."""
    logger.info("Starting model training")
    
    # Create model
    model = create_sample_model()
    
    # Generate sample data
    X_train, y_train = generate_sample_data()
    
    # Split data
    split_idx = int(0.8 * len(X_train))
    X_train, X_val = X_train[:split_idx], X_train[split_idx:]
    y_train, y_val = y_train[:split_idx], y_train[split_idx:]
    
    # Train model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=5,
        batch_size=32,
        verbose=1
    )
    
    # Save model
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    model_path = models_dir / "kolam_detection_model.h5"
    model.save(model_path)
    
    logger.info(f"Model trained and saved to {model_path}")
    
    # Print training results
    final_accuracy = history.history['accuracy'][-1]
    final_val_accuracy = history.history['val_accuracy'][-1]
    
    print(f"✅ Training completed!")
    print(f"📊 Final training accuracy: {final_accuracy:.4f}")
    print(f"📊 Final validation accuracy: {final_val_accuracy:.4f}")
    print(f"💾 Model saved to: {model_path}")
    
    return model_path


def main():
    """Main training function."""
    try:
        model_path = train_model()
        print(f"🎯 Kolam detection model training completed successfully!")
        return 0
    except Exception as e:
        logger.error(f"Training failed: {e}")
        print(f"❌ Error during training: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

