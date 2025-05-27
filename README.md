# 🚁 Premiere FPV Transition Plugin

Adobe Premiere Pro plugin that transforms videos into immersive FPV drone-style perspectives with smooth 3D transitions and AI-powered frame interpolation.

## 🎯 Features

- **3D FPV Transformations**: Basic 3D rotations (X/Y/Z axes) and field of view adjustments
- **Smooth Transitions**: Fluid movement between clips with 3D interpolation
- **AI Frame Generation**: Fill missing frames (≤1 second gaps) using RIFE AI
- **Interactive Control Panel**: Adjust trajectory curvature, speed, and "FPV intensity"
- **GPU Accelerated**: Leverages CUDA for real-time performance

## 📋 Requirements

### Minimum Hardware
- NVIDIA GPU with 6GB+ VRAM
- 16GB RAM
- Windows 10/11 or macOS 12+

### Software
- Adobe Premiere Pro 2023 or later
- Python 3.8+
- CUDA Toolkit 11.7+

## 🛠️ Technology Stack

### Core 3D Engine
- **OpenCV 3D Module**: For rotation/perspective calculations
- **Three.js**: WebGL-based 3D preview in CEP panel

### AI Interpolation
- **RIFE v4.9**: Real-time frame interpolation
- **PyTorch**: GPU acceleration via CUDA

### Adobe Integration
- **ExtendScript**: Automate native 3D effects
- **Mercury Transmit**: GPU-Premiere data communication

## 📦 Installation

1. Download the latest `.ZXP` installer from [Releases](https://github.com/mauriale/premiere-fpv-transition-plugin/releases)
2. Install using [ZXP/UXP Installer](https://aescripts.com/learn/zxp-installer/)
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch Premiere Pro and find the plugin in Window > Extensions

## 🚀 Quick Start

1. Import your footage into Premiere Pro
2. Open the FPV Transition panel
3. Select clips and apply FPV transformation
4. Adjust parameters in the control panel
5. Generate transitions between clips
6. Export your immersive FPV video

## 📊 Performance Limits

- **Input Resolution**: Up to 4K @ 30fps (1080p recommended for AI processing)
- **Rotational Range**: ±45° on X/Y axes
- **Transition Duration**: 0.5-3 seconds optimal
- **VRAM Usage**: ~5% increase over baseline

## 🔧 Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## 📚 Documentation

- [User Guide](docs/USER_GUIDE.md)
- [API Reference](docs/API.md)
- [Video Tutorial](docs/tutorials/)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [RIFE](https://github.com/hzwer/arXiv2020-RIFE) for frame interpolation
- [OpenCV](https://opencv.org/) for 3D calculations
- [Three.js](https://threejs.org/) for WebGL rendering

---

**Note**: This plugin does not process audio. Audio tracks remain unchanged during transformation.