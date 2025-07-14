import grpc
import logging
from PIL import Image
import io
import argparse

# Import proto generated files
import liveness_api_pb2
import liveness_api_pb2_grpc

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LivenessClient:
    """Client untuk liveness detection service"""
    
    def __init__(self, server_address='localhost:50051'):
        """Initialize client"""
        self.server_address = server_address
        self.channel = grpc.insecure_channel(server_address)
        self.stub = liveness_api_pb2_grpc.LivenessServiceStub(self.channel)
        logger.info(f"Connected to server at {server_address}")
    
    def predict_liveness_from_file(self, image_path):
        """Predict liveness dari file gambar"""
        try:
            # Load dan convert image ke bytes
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            # Deteksi format dari ekstensi file
            image_format = image_path.split('.')[-1].upper()
            if image_format == 'JPG':
                image_format = 'JPEG'
            
            # Create request
            request = liveness_api_pb2.LivenessRequest(
                image_data=image_bytes,
                image_format=image_format
            )
            
            # Call service
            logger.info(f"Sending prediction request for {image_path}")
            response = self.stub.PredictLiveness(request)
            
            if response.success:
                logger.info("Prediction successful!")
                return {
                    "is_live": response.is_live,
                    "confidence": response.confidence,
                    "predicted_class": response.predicted_class,
                    "probabilities": {
                        "fake": response.probabilities.fake,
                        "live": response.probabilities.live
                    }
                }
            else:
                logger.error(f"Prediction failed: {response.error_message}")
                return None
                
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return None
    
    def get_model_status(self):
        """Get status model"""
        try:
            request = liveness_api_pb2.ModelStatusRequest()
            response = self.stub.GetModelStatus(request)
            
            return {
                "status": response.status,
                "model_name": response.model_name,
                "model_type": response.model_type,
                "local_path": response.local_path,
                "is_loaded": response.is_loaded
            }
            
        except Exception as e:
            logger.error(f"Error getting model status: {e}")
            return None
    
    def close(self):
        """Close connection"""
        self.channel.close()

def main():
    """Main function untuk testing"""
    parser = argparse.ArgumentParser(description='Liveness Detection Client')
    parser.add_argument('--image', '-i', help='Path ke file gambar untuk prediksi')
    parser.add_argument('--status', '-s', action='store_true', help='Cek status model')
    parser.add_argument('--server', default='localhost:50051', help='Server address')
    
    args = parser.parse_args()
    
    # Create client
    client = LivenessClient(args.server)
    
    try:
        if args.status:
            # Get model status
            status = client.get_model_status()
            if status:
                print("\n=== Model Status ===")
                print(f"Status: {status['status']}")
                print(f"Model Name: {status['model_name']}")
                print(f"Model Type: {status['model_type']}")
                print(f"Local Path: {status['local_path']}")
                print(f"Is Loaded: {status['is_loaded']}")
            else:
                print("Failed to get model status")
        
        if args.image:
            # Predict liveness
            result = client.predict_liveness_from_file(args.image)
            if result:
                print(f"\n=== Liveness Prediction Results ===")
                print(f"Image: {args.image}")
                print(f"Is Live: {result['is_live']}")
                print(f"Confidence: {result['confidence']:.3f}")
                print(f"Predicted Class: {result['predicted_class']}")
                print(f"Probabilities:")
                print(f"  - Fake: {result['probabilities']['fake']:.3f}")
                print(f"  - Live: {result['probabilities']['live']:.3f}")
            else:
                print("Prediction failed")
        
        if not args.image and not args.status:
            print("Please specify --image or --status")
            parser.print_help()
            
    finally:
        client.close()

if __name__ == "__main__":
    main() 