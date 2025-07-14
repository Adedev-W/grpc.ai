# DINOv2 Liveness Detection

This project uses the `nguyenkhoa/dinov2_Liveness_detection_v2.2.3` model from Hugging Face to detect whether an image shows a live person or a fake/spoof attempt.

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

#### Basic Usage
```bash
# Process a single image
python liveness_detection.py --image photo.jpg

# Process multiple images
python liveness_detection.py --images photo1.jpg photo2.png photo3.jpeg

# Process all images in a folder
python liveness_detection.py --folder ./test_images

# Save results to JSON file
python liveness_detection.py --image photo.jpg --output results.json
```

#### Save Model Locally
```bash
# Download and save model for offline use
python liveness_detection.py --image photo.jpg --save-model ./my_model

# Use locally saved model
python liveness_detection.py --image photo.jpg --model-path ./my_model --use-local
```

### Programmatic Usage

```python
from liveness_detection import LivenessDetector

# Initialize detector
detector = LivenessDetector()

# Process single image
result = detector.predict("photo.jpg")
print(f"Prediction: {result['predicted_class']}")
print(f"Confidence: {result['confidence']:.4f}")
print(f"Is Live: {result['is_live']}")

# Process multiple images
results = detector.predict_batch(["photo1.jpg", "photo2.jpg"])

# Save model locally
detector.save_model("./saved_model")

# Use local model
local_detector = LivenessDetector("./saved_model", use_local=True)
```

## Output Format

The model returns results in the following format:

```json
{
  "image_path": "photo.jpg",
  "predicted_class": "live",
  "predicted_class_id": 1,
  "confidence": 0.8934,
  "is_live": true,
  "all_scores": {
    "fake": 0.1066,
    "live": 0.8934
  }
}
```

## Features

- **GPU Support**: Automatically uses CUDA if available
- **Batch Processing**: Process multiple images efficiently
- **Local Model Saving**: Download and save models for offline use
- **Flexible Input**: Support for single images, multiple images, or entire folders
- **JSON Output**: Save results to JSON files for further processing
- **Confidence Scores**: Get confidence scores for all classes

## Files

- `liveness_detection.py`: Main script with LivenessDetector class
- `example_usage.py`: Example showing programmatic usage
- `requirements.txt`: Required Python packages
- `README.md`: This documentation

## Model Information

This implementation uses the `nguyenkhoa/dinov2_Liveness_detection_v2.2.3` model, which is based on DINOv2 (self-supervised Vision Transformer) for liveness detection.

The model classifies images into two categories:
- **Live**: Real, live person
- **Fake**: Photo, video, or other spoof attempt