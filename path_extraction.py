import cv2
import numpy as np
from skimage import measure
import matplotlib.pyplot as plt

def extract_paths_from_sketch(image):
    """
    Extract paths from a sketch image using OpenCV
    
    Args:
        image: Input image as numpy array (BGR format)
        
    Returns:
        processed_image: Visualization of the processed image
        paths: List of extracted paths as coordinate points
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding to handle different lighting conditions
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Perform morphological operations to clean up the image
    kernel = np.ones((3, 3), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # Skeletonize the image to get thin lines
    skeleton = skeletonize(cleaned)
    
    # Find contours in the skeletonized image
    contours, _ = cv2.findContours(
        skeleton.astype(np.uint8), 
        cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_NONE
    )
    
    # Create a visualization image
    vis_image = image.copy()
    cv2.drawContours(vis_image, contours, -1, (0, 255, 0), 2)
    
    # Extract paths from contours
    paths = []
    for contour in contours:
        if len(contour) > 10:  # Filter out very small contours
            # Simplify contour to reduce number of points
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Extract points from the contour
            points = []
            for point in approx:
                x, y = point[0]
                points.append((x, y))
            
            paths.append(points)
    
    return vis_image, paths

def skeletonize(img):
    """
    Skeletonize a binary image using morphological operations
    """
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False
    
    while not done:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()
        
        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True
    
    return skel

def visualize_paths(image, paths):
    """
    Create a visualization of the extracted paths
    
    Args:
        image: Original image
        paths: List of paths as coordinate points
        
    Returns:
        vis_image: Visualization image with paths drawn
    """
    vis_image = image.copy()
    
    # Draw each path with a different color
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
    ]
    
    for i, path in enumerate(paths):
        color = colors[i % len(colors)]
        
        # Draw the path
        for j in range(len(path) - 1):
            pt1 = tuple(map(int, path[j]))
            pt2 = tuple(map(int, path[j + 1]))
            cv2.line(vis_image, pt1, pt2, color, 2)
        
        # Draw points
        for point in path:
            x, y = map(int, point)
            cv2.circle(vis_image, (x, y), 5, color, -1)
    
    return vis_image

def extract_dimensions(image, paths):
    """
    Attempt to extract dimensions from the sketch
    This is a placeholder for more advanced dimension extraction
    
    Args:
        image: Original image
        paths: List of paths as coordinate points
        
    Returns:
        dimensions: Dictionary of extracted dimensions
    """
    # This is a simplified placeholder
    # In a real implementation, we would:
    # 1. Detect text using OCR
    # 2. Associate text with nearby lines
    # 3. Parse dimension values
    
    dimensions = {}
    
    # For now, just calculate the bounding box of each path
    for i, path in enumerate(paths):
        if path:
            xs = [p[0] for p in path]
            ys = [p[1] for p in path]
            width = max(xs) - min(xs)
            height = max(ys) - min(ys)
            dimensions[f"path_{i}"] = {
                "width": width,
                "height": height,
                "length": sum(
                    np.sqrt((path[j][0] - path[j-1][0])**2 + (path[j][1] - path[j-1][1])**2)
                    for j in range(1, len(path))
                )
            }
    
    return dimensions