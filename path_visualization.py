import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from PIL import Image

def visualize_robot_path(paths, motion_types, figsize=(8, 6)):
    """
    Create a 2D visualization of the robot path
    
    Args:
        paths: List of paths as coordinate points
        motion_types: List of motion types used
        figsize: Figure size as (width, height) tuple
        
    Returns:
        fig: Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Define colors for different motion types
    motion_colors = {
        "LIN": "blue",
        "PTP": "red",
        "CIRC": "green",
        "SPLINE": "purple"
    }
    
    # Plot each path
    for path_idx, path in enumerate(paths):
        if not path:
            continue
        
        # Extract x and y coordinates
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        
        # Plot the path
        ax.plot(xs, ys, 'k-', alpha=0.3, linewidth=1)
        
        # Plot points with motion type colors
        for i, (x, y) in enumerate(path):
            motion_type = motion_types[i % len(motion_types)]
            color = motion_colors.get(motion_type, "black")
            
            # Plot the point
            ax.scatter(x, y, color=color, s=50, zorder=10)
            
            # Add point label
            ax.text(x + 5, y + 5, f"P{i+1}", fontsize=8)
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=motion_type)
        for motion_type, color in motion_colors.items()
        if motion_type in motion_types
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # Set labels and title
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_title('Robot Path Visualization')
    
    # Invert y-axis to match image coordinates
    ax.invert_yaxis()
    
    # Set equal aspect ratio
    ax.set_aspect('equal')
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    return fig

def get_visualization_as_image(fig):
    """
    Convert a matplotlib figure to a PIL Image
    
    Args:
        fig: Matplotlib figure object
        
    Returns:
        image: PIL Image object
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    return img

def get_visualization_as_base64(fig):
    """
    Convert a matplotlib figure to a base64 encoded string
    
    Args:
        fig: Matplotlib figure object
        
    Returns:
        base64_image: Base64 encoded image string
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode()
    return img_str

def overlay_path_on_image(image, paths, motion_types):
    """
    Overlay the robot path on the original image
    
    Args:
        image: Original image as numpy array
        paths: List of paths as coordinate points
        motion_types: List of motion types used
        
    Returns:
        overlay_image: Image with path overlay
    """
    # Create a copy of the image
    overlay = image.copy()
    
    # Define colors for different motion types (BGR format for OpenCV)
    motion_colors = {
        "LIN": (255, 0, 0),    # Blue
        "PTP": (0, 0, 255),    # Red
        "CIRC": (0, 255, 0),   # Green
        "SPLINE": (255, 0, 255)  # Purple
    }
    
    # Draw each path
    for path_idx, path in enumerate(paths):
        if not path:
            continue
        
        # Draw lines connecting points
        for i in range(len(path) - 1):
            pt1 = tuple(map(int, path[i]))
            pt2 = tuple(map(int, path[i + 1]))
            
            # Get motion type for this segment
            motion_type = motion_types[i % len(motion_types)]
            color = motion_colors.get(motion_type, (0, 0, 0))
            
            # Draw line
            import cv2
            cv2.line(overlay, pt1, pt2, color, 2)
        
        # Draw points
        for i, point in enumerate(path):
            x, y = map(int, point)
            
            # Get motion type for this point
            motion_type = motion_types[i % len(motion_types)]
            color = motion_colors.get(motion_type, (0, 0, 0))
            
            # Draw circle
            import cv2
            cv2.circle(overlay, (x, y), 5, color, -1)
            
            # Add point label
            cv2.putText(overlay, f"P{i+1}", (x + 5, y + 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    return overlay