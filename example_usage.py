#!/usr/bin/env python3
"""
Example usage of the LivenessDetector class.
This script demonstrates how to use the liveness detection model programmatically.
"""

from liveness_detection import LivenessDetector
import os

def main():
    # Initialize the detector
    print("Initializing Liveness Detector...")
    detector = LivenessDetector()
    
    # Save the model locally (optional)
    print("\nSaving model locally...")
    detector.save_model("./saved_model")
    
    # Example 1: Process a single image
    print("\n=== Example 1: Single Image ===")
    # Replace with your actual image path
    image_path = "example_image.jpg"
    
    if os.path.exists(image_path):
        result = detector.predict(image_path)
        if result:
            print(f"Image: {result['image_path']}")
            print(f"Prediction: {result['predicted_class']}")
            print(f"Confidence: {result['confidence']:.4f}")
            print(f"Is Live: {result['is_live']}")
            print("All scores:")
            for label, score in result['all_scores'].items():
                print(f"  {label}: {score:.4f}")
    else:
        print(f"Image file {image_path} not found. Please provide a valid image path.")
    
    # Example 2: Process multiple images
    print("\n=== Example 2: Multiple Images ===")
    image_paths = ["image1.jpg", "image2.png", "image3.jpeg"]
    
    # Filter to existing files
    existing_images = [path for path in image_paths if os.path.exists(path)]
    
    if existing_images:
        results = detector.predict_batch(existing_images)
        for result in results:
            print(f"\nImage: {result['image_path']}")
            print(f"Prediction: {result['predicted_class']} (confidence: {result['confidence']:.4f})")
    else:
        print("No valid image files found in the list.")
    
    # Example 3: Using locally saved model
    print("\n=== Example 3: Using Local Model ===")
    if os.path.exists("./saved_model"):
        local_detector = LivenessDetector(model_path="./saved_model", use_local=True)
        print("Successfully loaded model from local directory!")
    else:
        print("No local model found. Run the detector.save_model() first.")
    
    print("\nExample completed!")

if __name__ == "__main__":
    main()