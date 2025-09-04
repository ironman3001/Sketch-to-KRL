# Sketch-to-KRL Code Generator

A Python-based web application that converts sketches of robot paths into KUKA Robot Language (KRL) code.

## Features

- **Sketch Input**:
  - Upload PNG/JPG sketches with dimensions
  - Draw sketches directly in the browser canvas
  - Convert sketches into edge/path representation using OpenCV

- **Interactive Q&A Flow**:
  - Configure start position (HOME or Anywhere)
  - Select motion types (LIN, PTP, CIRC, SPLINE)
  - Enable path smoothing and dimension extraction
  - Adjust path simplification

- **KRL Code Generation**:
  - Auto-generate KRL program structure
  - Insert motion commands based on user input
  - Generate both .src and .dat files

- **Output and Visualization**:
  - Display generated KRL code
  - Download .src and .dat files
  - 2D visualization of extracted path on the sketch

## Installation

### Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/sketch-to-krl.git
   cd sketch-to-krl
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

### Google Colab

1. Open the `sketch_to_krl_colab.ipynb` notebook in Google Colab
2. Run all cells in the notebook
3. Click on the generated URL to access the application

### Hugging Face Spaces

The application is also available on Hugging Face Spaces:
1. Visit [Hugging Face Spaces](https://huggingface.co/spaces)
2. Search for "Sketch-to-KRL Code Generator"
3. Open the application

## Usage

1. **Upload or Draw a Sketch**:
   - Upload a PNG/JPG file containing a robot path sketch
   - Or use the drawing canvas to create a path

2. **Configure Robot Path**:
   - Select start position (HOME or Anywhere)
   - Choose motion types (LIN, PTP, CIRC, SPLINE)
   - Enable additional options if needed

3. **Generate KRL Code**:
   - Click "Generate KRL Code" to process the sketch
   - View the generated code and path visualization
   - Download the .src and .dat files

## Example Sketches

The repository includes several example sketches for testing:

- Square with diagonal
- Circle
- Star
- Zigzag
- Spiral

These can be found in the `test_sketches` directory.

## KRL Code Structure

The generated KRL code follows this structure:

```
DEF PATH_PROGRAM()
   BAS (#INITMOV,0)
   PTP HOME
   LIN P1
   CIRC P2, P3
   SPL P4
   PTP HOME
END
```

The corresponding DAT file contains point definitions:

```
&ACCESS RVP
&REL 1
&PARAM TEMPLATE = C_PTP
&PARAM EDITMASK = *
DEFDAT PATH_PROGRAM

DECL E6POS XHOME={X 0.0,Y 0.0,Z 0.0,A 0.0,B 0.0,C 0.0}
DECL E6POS P1={X 100.0,Y 200.0,Z 100.0,A 0.0,B 90.0,C 0.0}
DECL E6POS P2={X 200.0,Y 300.0,Z 120.0,A 0.0,B 90.0,C 0.0}
DECL E6POS P3={X 300.0,Y 200.0,Z 80.0,A 0.0,B 90.0,C 0.0}

ENDDAT
```

## Project Structure

- `app.py`: Main Streamlit application
- `path_extraction.py`: Functions for extracting paths from sketches
- `krl_generator.py`: KRL code generation logic
- `drawing_canvas.py`: Interactive drawing canvas component
- `path_visualization.py`: Path visualization utilities
- `file_utils.py`: File handling utilities
- `requirements.txt`: Required Python packages
- `test_sketches/`: Example sketches for testing

## Requirements

- Python 3.10+
- Streamlit
- OpenCV
- NumPy
- Pillow
- Matplotlib
- scikit-image

## License

This project is licensed under the MIT License - see the LICENSE file for details.