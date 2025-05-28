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
    try:
        subprocess.run([sys.executable, "scripts/install_dependencies.py"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️  Warning: Some dependencies failed to install")
        print("   You may need to install them manually")
    
    print("\n2. Building plugin...")
    try:
        subprocess.run([sys.executable, "scripts/build_plugin.py"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️  Warning: Build completed with errors")
    
    print("\n3. Starting backend server...")
    print("   Server will run at http://localhost:8080")
    print("   Press Ctrl+C to stop")
    
    # Change to src directory and start the server
    src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
    os.chdir(src_dir)
    
    # Start the backend server
    try:
        subprocess.run([sys.executable, "backend/server.py"])
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped.")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nTo start the server manually:")
        print(f"  cd {src_dir}")
        print("  python backend/server.py")

if __name__ == "__main__":
    main()