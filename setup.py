#!/usr/bin/env python3
"""
Setup script for Stop Motion Video Processor
"""

import subprocess
import sys
import os

def install_requirements():
    """Install Python requirements."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Python dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False
    return True

def check_opencv():
    """Check if OpenCV is working properly."""
    try:
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
        return True
    except ImportError:
        print("❌ OpenCV not installed or not working")
        return False

def create_directories():
    """Create necessary directories."""
    dirs = ['uploads', 'outputs', 'templates', 'static']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✅ Created necessary directories")

def main():
    print("🎬 Setting up Stop Motion Video Processor...")
    print()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check OpenCV
    if not check_opencv():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print()
    print("🎉 Setup complete!")
    print()
    print("To run the application:")
    print("  python app.py")
    print()
    print("Then open your browser to: http://localhost:8000")

if __name__ == "__main__":
    main()