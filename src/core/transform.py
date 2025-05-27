"""FPV transformation utilities using OpenCV."""

import cv2
import numpy as np
from typing import Tuple, List


class FPVTransform:
    """Handles 3D transformations for FPV effect."""
    
    def __init__(self, frame_width: int, frame_height: int):
        self.width = frame_width
        self.height = frame_height
        self.camera_matrix = self._create_camera_matrix()
    
    def _create_camera_matrix(self) -> np.ndarray:
        """Create camera intrinsic matrix."""
        focal_length = self.width
        center = (self.width / 2, self.height / 2)
        return np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype=float)
    
    def apply_rotation(self, frame: np.ndarray, 
                      rotation: Tuple[float, float, float]) -> np.ndarray:
        """Apply 3D rotation to frame.
        
        Args:
            frame: Input frame
            rotation: (x, y, z) rotation angles in degrees
        
        Returns:
            Transformed frame
        """
        # Convert rotation to radians
        rx, ry, rz = [np.radians(angle) for angle in rotation]
        
        # Create rotation matrix
        rotation_vector = np.array([rx, ry, rz])
        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        
        # Apply perspective transformation
        h, w = frame.shape[:2]
        transform_matrix = self.camera_matrix @ rotation_matrix @ np.linalg.inv(self.camera_matrix)
        
        # Warp perspective
        result = cv2.warpPerspective(frame, transform_matrix, (w, h))
        
        return result
    
    def adjust_fov(self, frame: np.ndarray, fov_factor: float) -> np.ndarray:
        """Adjust field of view.
        
        Args:
            frame: Input frame
            fov_factor: FOV adjustment factor (0.5-2.0)
        
        Returns:
            Frame with adjusted FOV
        """
        h, w = frame.shape[:2]
        
        # Create scaling matrix
        scale_matrix = np.array([
            [fov_factor, 0, w * (1 - fov_factor) / 2],
            [0, fov_factor, h * (1 - fov_factor) / 2],
            [0, 0, 1]
        ])
        
        # Apply transformation
        result = cv2.warpPerspective(frame, scale_matrix, (w, h))
        
        return result