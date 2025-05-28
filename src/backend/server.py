"""Backend server for handling AI processing requests."""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
from pathlib import Path
import numpy as np

# Import relative modules properly
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.transform import FPVTransform
from core.interpolation import trajectory_interpolate
from ai.rife_wrapper import RIFEInterpolator

app = Flask(__name__)
CORS(app)

# Load configuration
config_path = Path(__file__).parent.parent.parent / 'config' / 'default.json'
if config_path.exists():
    with open(config_path, 'r') as f:
        config = json.load(f)
else:
    # Default config if file not found
    config = {
        'device': {'use_cuda': False, 'vram_mb': 4096},
        'logging': {'log_level': 'info', 'log_file': 'fpv_plugin.log'}
    }

# Setup logging
logging.basicConfig(
    level=getattr(logging, config['logging']['log_level'].upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=config['logging']['log_file']
)
logger = logging.getLogger(__name__)

# Initialize components
transform = None
interpolator = None

# Check GPU availability
try:
    import torch
    if torch.cuda.is_available() and config['device']['use_cuda']:
        device = 'cuda'
        logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
        logger.info(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        device = 'cpu'
        logger.warning("CUDA not available, falling back to CPU")
except ImportError:
    device = 'cpu'
    logger.warning("PyTorch not installed, using CPU only")


@app.route('/api/status', methods=['GET'])
def status():
    """Get server status and hardware info."""
    return jsonify({
        'status': 'running',
        'device': device,
        'gpu_available': device == 'cuda',
        'vram_mb': config['device']['vram_mb'],
        'config': config
    })


@app.route('/api/transition', methods=['POST'])
def create_transition():
    """Create transition between clips."""
    try:
        data = request.json
        start_rotation = data.get('start_rotation', [0, 0, 0])
        end_rotation = data.get('end_rotation', [0, 0, 0])
        duration = data.get('duration', 1.0)
        intensity = data.get('intensity', 'medium')
        
        logger.info(f"Creating transition: {start_rotation} -> {end_rotation}, duration: {duration}s")
        
        # Calculate number of interpolation steps
        fps = 30  # Assume 30fps
        num_frames = int(duration * fps)
        
        # Check if we need to limit frames for GTX 1650
        if config['device']['vram_mb'] < 6000 and num_frames > 30:
            logger.warning(f"Limiting frames from {num_frames} to 30 for GTX 1650")
            num_frames = 30
        
        # Generate interpolated rotation matrices
        # Convert rotation angles to matrices
        start_mat = _rotation_angles_to_matrix(start_rotation)
        end_mat = _rotation_angles_to_matrix(end_rotation)
        
        # Interpolate
        interpolated_matrices = trajectory_interpolate(start_mat, end_mat, num_frames)
        
        # Convert back to angles for ExtendScript
        interpolated_angles = [_matrix_to_rotation_angles(mat) for mat in interpolated_matrices]
        
        return jsonify({
            'success': True,
            'frames': num_frames,
            'keyframes': interpolated_angles,
            'message': 'Transition created successfully'
        })
        
    except Exception as e:
        logger.error(f"Error creating transition: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/transform', methods=['POST'])
def transform_frame():
    """Apply FPV transformation to a single frame."""
    global transform
    
    try:
        if 'frame' not in request.files:
            return jsonify({'error': 'Frame required'}), 400
        
        # Read frame
        frame = _file_to_numpy(request.files['frame'])
        h, w = frame.shape[:2]
        
        # Initialize transform if needed
        if transform is None:
            transform = FPVTransform(w, h)
        
        # Get transformation parameters
        rotation = [
            float(request.form.get('tilt', 0)),
            float(request.form.get('pan', 0)),
            float(request.form.get('roll', 0))
        ]
        fov_factor = float(request.form.get('fov', 1.0))
        
        # Apply transformations
        result = transform.apply_rotation(frame, rotation)
        result = transform.adjust_fov(result, fov_factor)
        
        # Convert to base64
        from PIL import Image
        import io
        import base64
        
        img = Image.fromarray(result.astype('uint8'))
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'frame': img_str
        })
        
    except Exception as e:
        logger.error(f"Error transforming frame: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def _file_to_numpy(file):
    """Convert uploaded file to numpy array."""
    from PIL import Image
    import io
    
    img = Image.open(io.BytesIO(file.read()))
    return np.array(img)


def _rotation_angles_to_matrix(angles):
    """Convert rotation angles to rotation matrix."""
    import cv2
    rx, ry, rz = [np.radians(a) for a in angles]
    rotation_vector = np.array([rx, ry, rz])
    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
    return rotation_matrix


def _matrix_to_rotation_angles(matrix):
    """Convert rotation matrix to angles."""
    import cv2
    rotation_vector, _ = cv2.Rodrigues(matrix)
    angles = [np.degrees(a) for a in rotation_vector.flatten()]
    return angles


if __name__ == '__main__':
    # Use lower port for development
    app.run(host='0.0.0.0', port=8080, debug=False)