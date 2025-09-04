# Sketch-to-KRL Code Generator Architecture

This document provides an overview of the architecture and key components of the Sketch-to-KRL Code Generator application.

## System Architecture

The application follows a modular architecture with the following components:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Sketch Input   │────▶│ Path Extraction │────▶│  KRL Generator  │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│ Drawing Canvas  │     │ Path Visualizer │     │  File Export    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Key Components

### 1. Main Application (`app.py`)

The main Streamlit application that orchestrates all components and provides the user interface. It manages:

- Application state and workflow
- User interface components
- Integration of all modules
- Session state management

### 2. Path Extraction (`path_extraction.py`)

Responsible for processing sketches and extracting path information:

- Converts images to grayscale
- Applies edge detection algorithms
- Extracts contours and paths
- Simplifies paths for robot motion

Key functions:
- `extract_paths_from_sketch()`: Processes an image and returns paths
- `skeletonize()`: Thins lines to single-pixel width
- `visualize_paths()`: Creates visualizations of extracted paths

### 3. KRL Generator (`krl_generator.py`)

Generates KUKA Robot Language code based on extracted paths:

- Creates program structure (.src file)
- Generates point definitions (.dat file)
- Maps motion types to path segments
- Handles different motion commands (LIN, PTP, CIRC, SPLINE)

Key methods:
- `generate_src_code()`: Creates the KRL program logic
- `generate_dat_code()`: Creates the point definitions

### 4. Drawing Canvas (`drawing_canvas.py`)

Provides an interactive canvas for users to draw robot paths:

- Supports different drawing modes (line, rectangle, circle)
- Manages canvas state
- Converts drawings to processable images

Key methods:
- `render()`: Displays the canvas and UI controls
- `reset_canvas()`: Clears the canvas
- `get_drawing_points()`: Returns points from the drawing

### 5. Path Visualization (`path_visualization.py`)

Creates visual representations of the robot paths:

- 2D path visualization with motion types
- Overlay of paths on original sketches
- Export of visualizations as images

Key functions:
- `visualize_robot_path()`: Creates a 2D plot of the path
- `overlay_path_on_image()`: Overlays the path on the original image

### 6. File Utilities (`file_utils.py`)

Handles file operations and downloads:

- Creates download links for generated files
- Packages multiple files into ZIP archives
- Manages file uploads and storage

Key functions:
- `get_download_link()`: Creates HTML download links
- `create_zip_download()`: Packages multiple files for download

## Data Flow

1. **Input Phase**:
   - User uploads an image or draws on the canvas
   - Image is processed to extract path information

2. **Configuration Phase**:
   - User selects start position, motion types, and options
   - Application stores these preferences

3. **Generation Phase**:
   - Path information and user preferences are used to generate KRL code
   - Both .src and .dat files are created

4. **Output Phase**:
   - Generated code is displayed to the user
   - Path visualizations are created
   - Download options are provided

## State Management

The application uses Streamlit's session state to manage application state:

- `current_step`: Tracks the current workflow step
- `processed_image`: Stores the processed sketch
- `extracted_paths`: Stores the extracted path data
- `motion_types`: Stores selected motion types
- `krl_code` and `dat_code`: Store generated code

## Technology Stack

- **Frontend**: Streamlit
- **Image Processing**: OpenCV, NumPy
- **Visualization**: Matplotlib
- **Drawing**: Pillow (PIL)
- **Path Analysis**: scikit-image

## Deployment Options

The application supports multiple deployment options:

1. **Local Deployment**: Running directly on a local machine
2. **Google Colab**: Running in a Colab notebook with public URL access
3. **Hugging Face Spaces**: Deployment as a Streamlit app on Hugging Face

## Future Enhancements

Potential areas for future development:

1. **Advanced Path Processing**:
   - Improved path smoothing algorithms
   - Better handling of intersections and overlaps

2. **3D Path Support**:
   - Extraction of 3D information from sketches
   - 3D visualization of robot paths

3. **Direct Robot Integration**:
   - Direct upload to KUKA robots
   - Simulation of generated paths

4. **Additional File Formats**:
   - Support for STL/DXF input
   - Export to additional robot languages