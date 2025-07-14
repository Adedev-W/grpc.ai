# Liveness Detection gRPC API

Sistem deteksi liveness menggunakan model DINOv2 yang dikemas dalam gRPC API. Project ini menggunakan model `nguyenkhoa/dinov2_Liveness_detection_v2.2.3` dari Hugging Face untuk membedakan antara wajah hidup (live) dan palsu (fake/spoof).

## 🚀 Fitur

- **Model Loading Sekali**: Model di-load hanya sekali saat startup menggunakan singleton pattern
- **gRPC API**: Interface yang efisien dan type-safe
- **Auto Model Saving**: Model otomatis disimpan lokal setelah download pertama
- **Error Handling**: Comprehensive error handling dan logging
- **Client Ready**: Termasuk client untuk testing

## 🛠️ Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd proto_api
```

### 2. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate Protobuf Files

```bash
chmod +x generate_proto.sh
./generate_proto.sh
```

## 📋 Requirements

```
grpcio==1.60.0
grpcio-tools==1.60.0
protobuf==4.25.1
transformers
torch
torchvision
Pillow
numpy
```

## 🏃‍♂️ Cara Menjalankan

### 1. Start Server

```bash
python liveness_server.py
```

Server akan berjalan di `localhost:50051` dan otomatis:
- Download model dari Hugging Face (pertama kali)
- Simpan model ke direktori `./saved_model`
- Load model ke memory

### 2. Test dengan Client

#### Cek Status Model

```bash
python liveness_client.py --status
```

#### Prediksi Liveness

```bash
python liveness_client.py --image path/to/image.jpg
```

#### Contoh Output

```
=== Liveness Prediction Results ===
Image: test_image.jpg
Is Live: True
Confidence: 0.876
Predicted Class: live
Probabilities:
  - Fake: 0.124
  - Live: 0.876
```

## 📁 Struktur Project

```
proto_api/
├── model_manager.py         # Singleton class untuk model management
├── liveness_api.proto      # Protobuf definition
├── liveness_server.py      # gRPC server implementation
├── liveness_client.py      # Client untuk testing
├── generate_proto.sh       # Script generate protobuf files
├── requirements.txt        # Python dependencies
├── README.md              # Dokumentasi
└── saved_model/           # Model tersimpan (auto-generated)
```

## 🔧 API Reference

### Service: LivenessService

#### 1. PredictLiveness

**Request:**
```protobuf
message LivenessRequest {
    bytes image_data = 1;      // Image dalam format bytes
    string image_format = 2;   // Format image (jpg, png, etc)
}
```

**Response:**
```protobuf
message LivenessResponse {
    bool is_live = 1;                    // True jika live, False jika fake
    float confidence = 2;                // Confidence score (0-1)
    string predicted_class = 3;          // "live" atau "fake"
    LivenessProbabilities probabilities = 4;  // Probabilitas detail
    bool success = 5;                    // Status success
    string error_message = 6;            // Error message jika ada
}
```

#### 2. GetModelStatus

**Request:**
```protobuf
message ModelStatusRequest {
    // Empty request
}
```

**Response:**
```protobuf
message ModelStatusResponse {
    string status = 1;        // "loaded", "not_loaded", "error"
    string model_name = 2;    // Nama model
    string model_type = 3;    // Tipe model
    string local_path = 4;    // Path model lokal
    bool is_loaded = 5;       // Status loading
}
```

## 🎯 Cara Kerja

1. **Model Loading**: Saat server start, `LivenessModelManager` (singleton) akan:
   - Cek apakah model sudah ada di `./saved_model`
   - Jika tidak, download dari Hugging Face
   - Simpan model ke lokal untuk penggunaan selanjutnya
   - Load model ke memory

2. **Prediction**: Ketika ada request:
   - Convert image bytes ke PIL Image
   - Preprocess menggunakan AutoImageProcessor
   - Inference menggunakan model
   - Return hasil prediksi

3. **Singleton Pattern**: Model hanya di-load sekali, request selanjutnya menggunakan model yang sama

## 🐛 Troubleshooting

### Model Loading Error

```bash
# Hapus model dan download ulang
rm -rf saved_model/
python liveness_server.py
```

### Protobuf Generation Error

```bash
# Install grpcio-tools
pip install grpcio-tools

# Generate ulang
./generate_proto.sh
```

### Server Port Already in Use

```bash
# Cari process yang menggunakan port 50051
lsof -i :50051

# Kill process
kill -9 <PID>
```

## 📊 Performance

- **Cold Start**: ~10-30 detik (download + load model)
- **Warm Start**: ~2-5 detik (load model dari lokal)
- **Inference**: ~100-500ms per image
- **Memory Usage**: ~2-4GB (tergantung model)

## 🔒 Security Notes

- Server berjalan tanpa SSL (development only)
- Untuk production, gunakan SSL/TLS
- Validasi input image size dan format
- Implementasi rate limiting jika diperlukan

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Model: [nguyenkhoa/dinov2_Liveness_detection_v2.2.3](https://huggingface.co/nguyenkhoa/dinov2_Liveness_detection_v2.2.3)
- Framework: Hugging Face Transformers
- gRPC: Google gRPC 