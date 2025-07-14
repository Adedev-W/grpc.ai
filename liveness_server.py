import grpc
from concurrent import futures
import logging
import io
from PIL import Image

# Import proto generated files (akan di-generate)
import liveness_api_pb2
import liveness_api_pb2_grpc

# Import model manager
from model_manager import model_manager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LivenessServicer(liveness_api_pb2_grpc.LivenessServiceServicer):
    """Implementasi service untuk liveness detection"""
    
    def __init__(self):
        """Initialize servicer dan pastikan model sudah loaded"""
        logger.info("Initializing LivenessServicer...")
        
        # Pastikan model sudah di-load
        if not model_manager.is_model_loaded():
            logger.info("Model belum loaded, loading sekarang...")
            model_manager.load_model()
        
        logger.info("LivenessServicer ready!")
    
    def PredictLiveness(self, request, context):
        """Predict liveness dari image bytes"""
        try:
            logger.info("Received liveness prediction request")
            
            # Convert bytes ke PIL Image
            image_bytes = request.image_data
            image_format = request.image_format or "JPEG"
            
            # Create PIL Image dari bytes
            image_stream = io.BytesIO(image_bytes)
            image = Image.open(image_stream)
            
            # Prediksi menggunakan model
            result = model_manager.predict_liveness(image)
            
            # Create response
            response = liveness_api_pb2.LivenessResponse(
                is_live=result["is_live"],
                confidence=result["confidence"],
                predicted_class=result["predicted_class"],
                probabilities=liveness_api_pb2.LivenessProbabilities(
                    fake=result["probabilities"]["fake"],
                    live=result["probabilities"]["live"]
                ),
                success=True,
                error_message=""
            )
            
            logger.info(f"Prediction completed: is_live={result['is_live']}, confidence={result['confidence']:.3f}")
            return response
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            
            # Return error response
            return liveness_api_pb2.LivenessResponse(
                is_live=False,
                confidence=0.0,
                predicted_class="error",
                probabilities=liveness_api_pb2.LivenessProbabilities(fake=0.0, live=0.0),
                success=False,
                error_message=str(e)
            )
    
    def GetModelStatus(self, request, context):
        """Get status model"""
        try:
            model_info = model_manager.get_model_info()
            
            response = liveness_api_pb2.ModelStatusResponse(
                status=model_info["status"],
                model_name=model_info.get("model_name", ""),
                model_type=model_info.get("model_type", ""),
                local_path=model_info.get("local_path", ""),
                is_loaded=model_manager.is_model_loaded()
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting model status: {e}")
            return liveness_api_pb2.ModelStatusResponse(
                status="error",
                model_name="",
                model_type="",
                local_path="",
                is_loaded=False
            )

def serve():
    """Start gRPC server"""
    # Create server dengan thread pool
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.keepalive_time_ms', 30000),
            ('grpc.keepalive_timeout_ms', 5000),
            ('grpc.keepalive_permit_without_calls', True),
            ('grpc.http2.max_pings_without_data', 0),
            ('grpc.http2.min_time_between_pings_ms', 10000),
            ('grpc.http2.min_ping_interval_without_data_ms', 300000)
        ]
    )
    
    # Add servicer
    liveness_api_pb2_grpc.add_LivenessServiceServicer_to_server(
        LivenessServicer(), server
    )
    
    # Start server
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    
    logger.info(f"Starting liveness detection server on {listen_addr}")
    server.start()
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)

if __name__ == "__main__":
    serve() 