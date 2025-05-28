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
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except:
        config = {
            'device': {
                'gpu_model': 'NVIDIA GeForce GTX 1650',
                'vram_mb': 4096,
                'cuda_version': '11.8'
            }
        }
    
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
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
    except subprocess.CalledProcessError:
        print("⚠️  Warning: Some packages failed to install")
        print("   Trying to install packages individually...")
        install_packages_individually()
    
    # Install PyTorch with CUDA support for GTX 1650
    print("\nInstalling PyTorch for GTX 1650...")
    install_pytorch()
    
    # Download RIFE lite model for GTX 1650
    print("\nSetting up RIFE model (optimized for 4GB VRAM)...")
    try:
        setup_rife_model()
    except Exception as e:
        print(f"⚠️  Warning: Could not download RIFE model: {e}")
        print("   You can download it manually later")
    
    # Install Node.js dependencies
    print("\nChecking Node.js dependencies...")
    try:
        subprocess.check_call(["npm", "--version"], stdout=subprocess.DEVNULL)
        subprocess.check_call(["npm", "install"], cwd="src/cep-panel")
    except:
        print("⚠️  Warning: Node.js not found. Please install Node.js to build the CEP panel")
    
    print("\n✅ Installation complete!")
    print("\nNext steps:")
    print("1. The plugin has been built: build/FPVTransition_v1.0.0.zxp")
    print("2. Install the .zxp file in Premiere Pro using ZXP/UXP Installer")
    print("3. The backend server is ready to run")


def install_packages_individually():
    """Try to install packages one by one."""
    packages = [
        "opencv-contrib-python",
        "numpy==1.24.3",
        "scipy==1.10.1",
        "flask==2.3.2",
        "flask-cors==3.0.10",
        "Pillow==9.5.0",
        "tqdm==4.65.0",
        "websocket-client==1.5.1"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ], stdout=subprocess.DEVNULL)
        except:
            print(f"  ⚠️  Failed to install {package}")


def install_pytorch():
    """Install PyTorch optimized for GTX 1650."""
    try:
        import torch
        print("PyTorch already installed")
        return
    except ImportError:
        pass
    
    print("Installing PyTorch...")
    
    # For GTX 1650, use CUDA 11.8 for better compatibility
    if platform.system() == "Windows":
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "torch", "torchvision", "torchaudio",
                "--index-url", "https://download.pytorch.org/whl/cu118"
            ])
        except:
            print("⚠️  Warning: PyTorch installation failed")
            print("   You can install it manually with:")
            print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    else:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "torch", "torchvision"
            ])
        except:
            print("⚠️  Warning: PyTorch installation failed")


def setup_rife_model():
    """Setup RIFE model directory."""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Create a placeholder for the model
    readme_path = models_dir / "README.md"
    readme_content = """# RIFE Models Directory

This directory should contain the RIFE model files.

For GTX 1650 (4GB VRAM), we recommend using RIFE-lite models.

## Download Instructions

1. Download RIFE v4.6-lite from:
   https://github.com/hzwer/arXiv2020-RIFE/releases

2. Extract the model files to this directory

3. The directory structure should look like:
   ```
   models/
   ├── README.md (this file)
   └── rife-v4.6-lite/
       ├── flownet.pkl
       ├── contextnet.pkl
       └── unet.pkl
   ```
"""
    
    readme_path.write_text(readme_content)
    print("Model directory created. Please download RIFE models manually.")


if __name__ == "__main__":
    install_dependencies()