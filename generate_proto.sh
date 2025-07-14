#!/bin/bash

# Generate Python files from proto
echo "Generating Python files from liveness_api.proto..."

python3 -m grpc_tools.protoc \
    --proto_path=. \
    --python_out=. \
    --grpc_python_out=. \
    liveness_api.proto

echo "Generated files:"
echo "- liveness_api_pb2.py"
echo "- liveness_api_pb2_grpc.py"
echo "Done!" 