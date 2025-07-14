#!/bin/bash

echo "🚀 Liveness Detection gRPC API - Deployment Script"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
MIN_VERSION="3.8"

if [ "$(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
    print_error "Python version $PYTHON_VERSION is too old. Please install Python 3.8 or higher."
    exit 1
fi

print_status "Python version: $PYTHON_VERSION ✓"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
else
    print_status "Virtual environment already exists ✓"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_status "Installing requirements..."
pip install -r requirements.txt

# Generate protobuf files
print_status "Generating protobuf files..."
if [ ! -f "liveness_api_pb2.py" ] || [ ! -f "liveness_api_pb2_grpc.py" ]; then
    chmod +x generate_proto.sh
    ./generate_proto.sh
else
    print_status "Protobuf files already exist ✓"
fi

# Check if protobuf files were generated successfully
if [ ! -f "liveness_api_pb2.py" ] || [ ! -f "liveness_api_pb2_grpc.py" ]; then
    print_error "Failed to generate protobuf files"
    exit 1
fi

print_status "Protobuf files generated successfully ✓"

# Create saved_model directory
if [ ! -d "saved_model" ]; then
    mkdir -p saved_model
    print_status "Created saved_model directory"
fi

# Run basic test
print_status "Running basic import test..."
python3 -c "
import sys
try:
    from model_manager import model_manager
    print('✓ model_manager imported successfully')
except Exception as e:
    print(f'✗ Error importing model_manager: {e}')
    sys.exit(1)

try:
    import liveness_api_pb2
    import liveness_api_pb2_grpc
    print('✓ protobuf files imported successfully')
except Exception as e:
    print(f'✗ Error importing protobuf files: {e}')
    sys.exit(1)

print('✓ All imports successful!')
"

if [ $? -eq 0 ]; then
    print_status "Basic test passed ✓"
else
    print_error "Basic test failed"
    exit 1
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "Next steps:"
echo "1. Start the server: python liveness_server.py"
echo "2. Test with client: python liveness_client.py --status"
echo "3. Make prediction: python liveness_client.py --image path/to/image.jpg"
echo ""
echo "Note: The model will be downloaded automatically on first run."
echo "This may take a few minutes depending on your internet connection." 