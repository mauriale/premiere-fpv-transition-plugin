#!/usr/bin/env python
"""
Quick start script for FPV Transition Plugin
Optimized for GTX 1650 (4GB VRAM)
"""

import subprocess
import sys
import os

def main():
    print("🚁 FPV Transition Plugin - Quick Start")
    print("=" * 50)
    print("Hardware: NVIDIA GTX 1650 (4GB VRAM)")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8+ required")
        sys.exit(1)
    
    print("\n1. Installing dependencies...")
    subprocess.run([sys.executable, "scripts/install_dependencies.py"])
    
    print("\n2. Building plugin...")
    subprocess.run([sys.executable, "scripts/build_plugin.py"])
    
    print("\n3. Starting backend server...")
    print("   Server will run at http://localhost:8080")
    print("   Press Ctrl+C to stop")
    
    # Start the backend server
    os.system("python -m src.backend.server")

if __name__ == "__main__":
    main()
