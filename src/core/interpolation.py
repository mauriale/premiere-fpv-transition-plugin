"""3D trajectory interpolation for smooth transitions."""

import numpy as np
import cv2
from typing import List, Tuple


def trajectory_interpolate(pose_a: np.ndarray, pose_b: np.ndarray, 
                         steps: int) -> List[np.ndarray]:
    """Interpolate between two 3D poses using SLERP.
    
    Args:
        pose_a: Starting pose (3x3 rotation matrix)
        pose_b: Ending pose (3x3 rotation matrix)
        steps: Number of interpolation steps
    
    Returns:
        List of interpolated rotation matrices
    """
    # Convert to rotation vectors
    rvec_a, _ = cv2.Rodrigues(pose_a)
    rvec_b, _ = cv2.Rodrigues(pose_b)
    
    # Interpolate rotation vectors
    interpolated_poses = []
    for t in np.linspace(0, 1, steps):
        # Linear interpolation of rotation vectors
        rvec_interp = (1 - t) * rvec_a + t * rvec_b
        
        # Convert back to rotation matrix
        rmat_interp, _ = cv2.Rodrigues(rvec_interp)
        interpolated_poses.append(rmat_interp)
    
    return interpolated_poses


def bezier_trajectory(control_points: List[Tuple[float, float, float]], 
                     steps: int) -> List[Tuple[float, float, float]]:
    """Generate smooth trajectory using Bezier curves.
    
    Args:
        control_points: List of (x, y, z) control points
        steps: Number of points to generate
    
    Returns:
        List of interpolated positions
    """
    n = len(control_points) - 1
    trajectory = []
    
    for t in np.linspace(0, 1, steps):
        point = np.zeros(3)
        for i, cp in enumerate(control_points):
            # Bernstein polynomial
            coeff = _bernstein_poly(i, n, t)
            point += coeff * np.array(cp)
        trajectory.append(tuple(point))
    
    return trajectory


def _bernstein_poly(i: int, n: int, t: float) -> float:
    """Calculate Bernstein polynomial coefficient."""
    from math import comb
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))