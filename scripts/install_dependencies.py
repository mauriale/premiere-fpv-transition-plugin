"""Install script for setting up dependencies optimized for GTX 1650."""

import subprocess
import sys
import platform
import json
from pathlib import Path


def install_dependencies():
    """Install Python dependencies with hardware-specific optimizations."""
    
    # Load configuration
    config_path = Path(__file__).parent.parent / 'config' / 'default.json'
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print("FPV Transition Plugin - Dependency Installer")
    print("="*50)
    print(f"Detected GPU: {config['device']['gpu_model']}")
    print(f"VRAM: {config['device']['vram_mb']} MB")
    print(f"CUDA Version: {config['device']['cuda_version']}")
    print("="*50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8+ required")
        sys.exit(1)
    
    # Install base requirements
    print("\nInstalling base requirements...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ])
    
    # Install PyTorch with CUDA support for GTX 1650
    print("\nInstalling PyTorch for CUDA 12.9...")
    if platform.system() == "Windows":
        # For GTX 1650, use CUDA 11.8 for better compatibility
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "torch==2.0.1+cu118",
            "torchvision==0.15.2+cu118",
            "--index-url", "https://download.pytorch.org/whl/cu118"
        ])
    else:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "torch==2.0.1",
            "torchvision==0.15.2"
        ])
    
    # Download RIFE lite model for GTX 1650
    print("\nDownloading RIFE-lite model (optimized for 4GB VRAM)...")
    download_rife_model()
    
    # Install Node.js dependencies
    print("\nInstalling Node.js dependencies...")
    subprocess.check_call(["npm", "install"], cwd="src/cep-panel")
    
    print("\n✅ Installation complete!")
    print("\nNext steps:")
    print("1. Run 'python scripts/build_plugin.py' to build the plugin")
    print("2. Install the .zxp file in Premiere Pro")
    print("3. Start the backend server: 'python -m src.backend.server'")


def download_rife_model():
    """Download RIFE model optimized for GTX 1650."""
    import urllib.request
    import zipfile
    import os
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Use RIFE-lite model for 4GB VRAM
    model_url = "https://github.com/hzwer/arXiv2020-RIFE/releases/download/v4.6/rife-v4.6-lite.zip"
    model_path = models_dir / "rife-v4.6-lite.zip"
    
    if not (models_dir / "rife-v4.6-lite").exists():
        print(f"Downloading from {model_url}...")
        urllib.request.urlretrieve(model_url, model_path)
        
        print("Extracting model...")
        with zipfile.ZipFile(model_path, 'r') as zip_ref:
            zip_ref.extractall(models_dir)
        
        os.remove(model_path)
        print("Model downloaded successfully!")
    else:
        print("Model already exists, skipping download.")


if __name__ == "__main__":
    install_dependencies()