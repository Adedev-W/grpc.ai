import os
import logging
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
from PIL import Image
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LivenessModelManager:
    """Singleton class untuk mengelola model liveness detection"""
    _instance = None
    _model = None
    _processor = None
    _model_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LivenessModelManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._model_loaded:
            self.load_model()
    
    def load_model(self):
        """Load model hanya sekali"""
        if self._model_loaded:
            logger.info("Model sudah di-load sebelumnya")
            return
            
        try:
            logger.info("Memulai loading model DINOv2 Liveness Detection...")
            
            # Cek apakah model sudah disimpan lokal
            local_model_path = "./saved_model"
            
            if os.path.exists(local_model_path):
                logger.info("Loading model dari direktori lokal...")
                self._processor = AutoImageProcessor.from_pretrained(local_model_path)
                self._model = AutoModelForImageClassification.from_pretrained(local_model_path)
            else:
                logger.info("Downloading model dari HuggingFace...")
                # Load model directly
                self._processor = AutoImageProcessor.from_pretrained(
                    "nguyenkhoa/dinov2_Liveness_detection_v2.2.3", 
                    use_fast=True
                )
                self._model = AutoModelForImageClassification.from_pretrained(
                    "nguyenkhoa/dinov2_Liveness_detection_v2.2.3"
                )
                
                # Simpan ke direktori lokal
                logger.info("Menyimpan model ke direktori lokal...")
                os.makedirs(local_model_path, exist_ok=True)
                self._model.save_pretrained(local_model_path)
                self._processor.save_pretrained(local_model_path)
                logger.info("Model berhasil disimpan ke ./saved_model")
            
            # Set model ke evaluation mode
            self._model.eval()
            self._model_loaded = True
            logger.info("Model berhasil di-load dan siap digunakan!")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise e
    
    def predict_liveness(self, image_path_or_pil):
        """
        Prediksi liveness dari gambar
        
        Args:
            image_path_or_pil: Path ke file gambar atau PIL Image object
            
        Returns:
            dict: {"is_live": bool, "confidence": float, "probabilities": dict}
        """
        if not self._model_loaded:
            raise RuntimeError("Model belum di-load!")
        
        try:
            # Load image
            if isinstance(image_path_or_pil, str):
                image = Image.open(image_path_or_pil).convert('RGB')
            else:
                image = image_path_or_pil.convert('RGB')
            
            # Preprocess image
            inputs = self._processor(image, return_tensors="pt")
            
            # Inference
            with torch.no_grad():
                outputs = self._model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits[0], dim=-1)
            
            # Get labels (biasanya 0: fake/spoof, 1: live)
            probabilities = predictions.cpu().numpy()
            predicted_class_id = probabilities.argmax().item()
            confidence = probabilities.max().item()
            
            # Mapping labels (sesuaikan dengan model yang digunakan)
            labels = {0: "fake", 1: "live"}
            predicted_label = labels.get(predicted_class_id, "unknown")
            
            result = {
                "is_live": predicted_label == "live",
                "confidence": float(confidence),
                "predicted_class": predicted_label,
                "probabilities": {
                    "fake": float(probabilities[0]),
                    "live": float(probabilities[1]) if len(probabilities) > 1 else 0.0
                }
            }
            
            logger.info(f"Prediction result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise e
    
    def is_model_loaded(self):
        """Cek apakah model sudah di-load"""
        return self._model_loaded
    
    def get_model_info(self):
        """Get informasi model"""
        if not self._model_loaded:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_name": "nguyenkhoa/dinov2_Liveness_detection_v2.2.3",
            "model_type": "AutoModelForImageClassification",
            "local_path": "./saved_model"
        }

# Create global instance
model_manager = LivenessModelManager() 