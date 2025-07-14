#!/usr/bin/env python3
"""
DINOv2 Liveness Detection Model Runner
This script loads and runs the nguyenkhoa/dinov2_Liveness_detection_v2.2.3 model
for detecting whether an image shows a live person or not.
"""

import os
import torch
from PIL import Image
import numpy as np
from transformers import AutoImageProcessor, AutoModelForImageClassification
import argparse
from pathlib import Path

class LivenessDetector:
    def __init__(self, model_path=None, use_local=False):
        """
        Initialize the liveness detection model.
        
        Args:
            model_path (str): Path to local model directory or HuggingFace model name
            use_local (bool): Whether to use locally saved model
        """
        if use_local and model_path and os.path.exists(model_path):
            print(f"Loading model from local path: {model_path}")
            self.processor = AutoImageProcessor.from_pretrained(model_path, use_fast=True)
            self.model = AutoModelForImageClassification.from_pretrained(model_path)
        else:
            model_name = model_path or "nguyenkhoa/dinov2_Liveness_detection_v2.2.3"
            print(f"Loading model from HuggingFace Hub: {model_name}")
            self.processor = AutoImageProcessor.from_pretrained(model_name, use_fast=True)
            self.model = AutoModelForImageClassification.from_pretrained(model_name)
        
        # Set model to evaluation mode
        self.model.eval()
        
        # Check if CUDA is available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        print(f"Model loaded on device: {self.device}")
        
        # Get class labels
        self.labels = self.model.config.id2label if hasattr(self.model.config, 'id2label') else {0: "fake", 1: "live"}
        print(f"Model labels: {self.labels}")
    
    def save_model(self, save_path="./saved_model"):
        """Save the model and processor to local directory."""
        print(f"Saving model to: {save_path}")
        os.makedirs(save_path, exist_ok=True)
        self.model.save_pretrained(save_path)
        self.processor.save_pretrained(save_path)
        print("Model saved successfully!")
    
    def preprocess_image(self, image_path):
        """
        Preprocess image for model input.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            torch.Tensor: Preprocessed image tensor
        """
        try:
            # Load and convert image to RGB
            image = Image.open(image_path).convert("RGB")
            
            # Process image using the processor
            inputs = self.processor(image, return_tensors="pt")
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            return inputs, image
        except Exception as e:
            print(f"Error preprocessing image {image_path}: {e}")
            return None, None
    
    def predict(self, image_path, return_confidence=True):
        """
        Predict liveness for a single image.
        
        Args:
            image_path (str): Path to the image file
            return_confidence (bool): Whether to return confidence scores
            
        Returns:
            dict: Prediction results
        """
        inputs, original_image = self.preprocess_image(image_path)
        if inputs is None:
            return None
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_class_id = predictions.argmax().item()
            confidence = predictions.max().item()
        
        result = {
            "image_path": image_path,
            "predicted_class": self.labels.get(predicted_class_id, f"class_{predicted_class_id}"),
            "predicted_class_id": predicted_class_id,
            "confidence": confidence,
            "is_live": predicted_class_id == 1 if 1 in self.labels else predicted_class_id == list(self.labels.keys())[1]
        }
        
        if return_confidence:
            result["all_scores"] = {self.labels.get(i, f"class_{i}"): float(predictions[0][i]) for i in range(len(predictions[0]))}
        
        return result
    
    def predict_batch(self, image_paths):
        """
        Predict liveness for multiple images.
        
        Args:
            image_paths (list): List of image file paths
            
        Returns:
            list: List of prediction results
        """
        results = []
        for image_path in image_paths:
            result = self.predict(image_path)
            if result:
                results.append(result)
        return results

def main():
    parser = argparse.ArgumentParser(description="Run DINOv2 Liveness Detection")
    parser.add_argument("--image", type=str, help="Path to single image file")
    parser.add_argument("--images", type=str, nargs="+", help="Paths to multiple image files")
    parser.add_argument("--folder", type=str, help="Path to folder containing images")
    parser.add_argument("--model-path", type=str, default="nguyenkhoa/dinov2_Liveness_detection_v2.2.3", 
                       help="Model path (HuggingFace name or local path)")
    parser.add_argument("--use-local", action="store_true", help="Use locally saved model")
    parser.add_argument("--save-model", type=str, help="Save model to specified directory")
    parser.add_argument("--output", type=str, help="Output file to save results (JSON)")
    
    args = parser.parse_args()
    
    # Initialize detector
    detector = LivenessDetector(args.model_path, args.use_local)
    
    # Save model if requested
    if args.save_model:
        detector.save_model(args.save_model)
    
    # Collect image paths
    image_paths = []
    
    if args.image:
        image_paths.append(args.image)
    
    if args.images:
        image_paths.extend(args.images)
    
    if args.folder:
        folder_path = Path(args.folder)
        supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        image_paths.extend([
            str(f) for f in folder_path.iterdir() 
            if f.is_file() and f.suffix.lower() in supported_extensions
        ])
    
    if not image_paths:
        print("No images specified. Use --image, --images, or --folder")
        print("\nExample usage:")
        print("python liveness_detection.py --image photo.jpg")
        print("python liveness_detection.py --folder ./test_images")
        print("python liveness_detection.py --image photo.jpg --save-model ./my_model")
        return
    
    # Run predictions
    print(f"\nProcessing {len(image_paths)} image(s)...")
    results = []
    
    for image_path in image_paths:
        print(f"\nProcessing: {image_path}")
        result = detector.predict(image_path)
        
        if result:
            results.append(result)
            print(f"  Prediction: {result['predicted_class']}")
            print(f"  Confidence: {result['confidence']:.4f}")
            print(f"  Is Live: {result['is_live']}")
            
            if 'all_scores' in result:
                print("  All scores:")
                for label, score in result['all_scores'].items():
                    print(f"    {label}: {score:.4f}")
        else:
            print(f"  Failed to process {image_path}")
    
    # Save results to file if requested
    if args.output and results:
        import json
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")
    
    # Summary
    if results:
        live_count = sum(1 for r in results if r['is_live'])
        fake_count = len(results) - live_count
        print(f"\nSummary:")
        print(f"  Total images: {len(results)}")
        print(f"  Live: {live_count}")
        print(f"  Fake: {fake_count}")

if __name__ == "__main__":
    main()