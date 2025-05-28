# Contributing to Premiere FPV Transition Plugin

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/premiere-fpv-transition-plugin.git
   cd premiere-fpv-transition-plugin
   ```

3. Install dependencies:
   ```bash
   # Python dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   
   # Node.js dependencies for CEP panel
   cd cep-panel
   npm install
   ```

4. Set up CEP debugging:
   - Enable debug mode in Premiere Pro
   - See [Adobe CEP Debugging Guide](https://github.com/Adobe-CEP/CEP-Resources/blob/master/CEP_10.x/Documentation/CEP%2010.0%20HTML%20Extension%20Cookbook.md#debugging)

## Project Structure

```
├── src/
│   ├── core/              # Core 3D processing
│   ├── ai/                # AI frame interpolation
│   ├── cep-panel/         # Adobe CEP panel
│   └── extendscript/      # ExtendScript files
├── tests/                 # Test suite
├── docs/                  # Documentation
└── examples/              # Example projects
```

## Pull Request Process

1. Create a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. Make your changes and commit:
   ```bash
   git commit -m 'Add amazing feature'
   ```

3. Run tests:
   ```bash
   pytest tests/
   ```

4. Push to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```

5. Open a Pull Request

## Code Style

- Python: Follow PEP 8, use Black formatter
- JavaScript: Use ESLint with provided config
- ExtendScript: Follow Adobe's style guide

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Test on both Windows and macOS if possible

## Reporting Issues

Use GitHub Issues to report bugs. Include:
- Premiere Pro version
- OS version
- GPU model
- Steps to reproduce
- Expected vs actual behavior

## License

By contributing, you agree that your contributions will be licensed under the MIT License.