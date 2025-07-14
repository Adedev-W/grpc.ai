# 🚀 Cara Deploy Project ke GitHub

Panduan lengkap untuk upload project Liveness Detection ke GitHub.

## 📋 Prerequisites

1. **Git** sudah terinstall
2. **Akun GitHub** sudah ada
3. **SSH Key** atau **Personal Access Token** sudah setup

### Cek Git Installation

```bash
git --version
```

Jika belum ada, install git:
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install git

# CentOS/RHEL
sudo yum install git
```

## 🔧 Step-by-Step Deployment

### 1. Initialize Git Repository

```bash
# Masuk ke direktori project
cd /home/As.Dev-ai/projectpy/proto_api

# Initialize git repository
git init

# Set user config (jika belum)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. Add Files ke Staging

```bash
# Add semua files (kecuali yang di .gitignore)
git add .

# Atau add files specific
git add README.md
git add requirements.txt
git add model_manager.py
git add liveness_api.proto
git add liveness_server.py
git add liveness_client.py
git add generate_proto.sh
git add deploy.sh
git add setup.py
git add .gitignore
```

### 3. Commit Changes

```bash
git commit -m "Initial commit: Liveness Detection gRPC API

Features:
- DINOv2 model integration
- Singleton pattern for model loading
- gRPC API with client/server
- Auto model download and saving
- Comprehensive error handling
- Docker ready setup"
```

### 4. Create Repository di GitHub

#### Option A: Via GitHub Web Interface

1. Buka [GitHub.com](https://github.com)
2. Login ke akun Anda
3. Klik **"+"** di pojok kanan atas
4. Pilih **"New repository"**
5. Isi form:
   - **Repository name**: `liveness-detection-grpc`
   - **Description**: `Liveness Detection API using DINOv2 model with gRPC`
   - **Visibility**: Public atau Private
   - **JANGAN** centang "Add README" (karena sudah ada)
6. Klik **"Create repository"**

#### Option B: Via GitHub CLI (jika ada)

```bash
gh repo create liveness-detection-grpc --public --description "Liveness Detection API using DINOv2 model with gRPC"
```

### 5. Connect Local Repository ke GitHub

```bash
# Add remote origin (ganti USERNAME dengan username GitHub Anda)
git remote add origin https://github.com/USERNAME/liveness-detection-grpc.git

# Atau jika pakai SSH
git remote add origin git@github.com:USERNAME/liveness-detection-grpc.git
```

### 6. Push ke GitHub

```bash
# Push ke main branch
git branch -M main
git push -u origin main
```

## 🔐 Authentication Options

### Option A: HTTPS dengan Personal Access Token

1. Buat Personal Access Token:
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token dengan scope `repo`
   
2. Saat push, gunakan token sebagai password:
   ```bash
   Username: your-username
   Password: your-personal-access-token
   ```

### Option B: SSH Key

1. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```

2. Add SSH key ke GitHub:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   Copy output dan add di GitHub → Settings → SSH and GPG keys

3. Test connection:
   ```bash
   ssh -T git@github.com
   ```

## 📝 Command Lengkap (Copy-Paste Ready)

```bash
# 1. Initialize dan setup
cd /home/As.Dev-ai/projectpy/proto_api
git init
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 2. Add dan commit
git add .
git commit -m "Initial commit: Liveness Detection gRPC API

Features:
- DINOv2 model integration  
- Singleton pattern for model loading
- gRPC API with client/server
- Auto model download and saving
- Comprehensive error handling"

# 3. Connect ke GitHub (ganti USERNAME)
git remote add origin https://github.com/USERNAME/liveness-detection-grpc.git

# 4. Push
git branch -M main
git push -u origin main
```

## 🔄 Update Project di GitHub

Setelah setup awal, untuk update selanjutnya:

```bash
# Add changes
git add .

# Commit dengan message yang descriptive
git commit -m "Add new feature: enhanced error handling"

# Push
git push
```

## 📁 Files yang Akan di-Upload

✅ **Yang AKAN di-upload:**
- `README.md` - Dokumentasi project
- `requirements.txt` - Dependencies
- `model_manager.py` - Model management
- `liveness_api.proto` - API definition
- `liveness_server.py` - gRPC server
- `liveness_client.py` - Client untuk testing
- `generate_proto.sh` - Script generate protobuf
- `deploy.sh` - Deployment script
- `setup.py` - Package setup
- `.gitignore` - Git ignore rules

❌ **Yang TIDAK akan di-upload** (karena .gitignore):
- `__pycache__/` - Python cache
- `venv/` - Virtual environment
- `saved_model/` - Model files (terlalu besar)
- `*_pb2.py` - Generated protobuf files
- Log files dan temporary files

## 🎯 Tips Deployment

1. **Model Size**: Model tidak di-upload ke GitHub karena terlalu besar. User akan download otomatis saat pertama kali run.

2. **Environment Variables**: Jika ada API keys, gunakan `.env` file dan tambahkan ke `.gitignore`.

3. **Documentation**: README.md sudah lengkap, update sesuai kebutuhan.

4. **Releases**: Setelah stable, buat release tags:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

5. **Issues & PR**: Enable issues dan pull requests di GitHub settings.

## 🔗 URL Repository

Setelah upload, repository akan tersedia di:
```
https://github.com/USERNAME/liveness-detection-grpc
```

Users bisa clone dengan:
```bash
git clone https://github.com/USERNAME/liveness-detection-grpc.git
cd liveness-detection-grpc
./deploy.sh
```

## 🐛 Troubleshooting

### Permission Denied

```bash
# Cek remote URL
git remote -v

# Ganti ke HTTPS jika SSH bermasalah
git remote set-url origin https://github.com/USERNAME/liveness-detection-grpc.git
```

### Large Files Error

```bash
# Jika ada file besar yang ter-commit, hapus dari history
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch saved_model/*' --prune-empty --tag-name-filter cat -- --all
```

### Authentication Failed

```bash
# Gunakan Personal Access Token sebagai password
# Atau setup SSH key seperti panduan di atas
```

---

**✨ Selamat! Project Anda sekarang sudah online di GitHub! ✨** 