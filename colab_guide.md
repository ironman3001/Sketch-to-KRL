# Running Sketch-to-KRL Code Generator in Google Colab

This guide explains how to run the Sketch-to-KRL Code Generator application in Google Colab.

## Overview

Google Colab provides a free environment to run Python code in the cloud. We'll use it to host our Streamlit application and make it accessible via a public URL.

## Step-by-Step Guide

### 1. Open the Notebook in Google Colab

1. Go to [Google Colab](https://colab.research.google.com/)
2. Click on "File" > "Open notebook"
3. Select the "GitHub" tab
4. Enter the GitHub repository URL or search for "sketch-to-krl"
5. Select the `sketch_to_krl_colab.ipynb` notebook

Alternatively, you can upload the `sketch_to_krl_colab.ipynb` file directly to Google Colab.

### 2. Run the Setup Cells

1. Run the first cell to install the required packages:
   ```python
   # Install required packages
   !pip install streamlit opencv-python numpy pillow matplotlib scikit-image
   ```

2. Run the cell to create the project directory:
   ```python
   # Create project directory
   !mkdir -p sketch_to_krl
   ```

### 3. Create Application Files

Run each of the code cells that create the application files:
- `app.py`
- `path_extraction.py`
- `krl_generator.py`
- `file_utils.py`
- `drawing_canvas.py`
- `path_visualization.py`
- `requirements.txt`

These cells use the `%%writefile` magic command to create the files in the Colab environment.

### 4. Run the Streamlit App

1. Run the cell that installs pyngrok:
   ```python
   # Install localtunnel
   !pip install pyngrok
   ```

2. Run the cell that starts the Streamlit app:
   ```python
   # Run the Streamlit app
   import os
   from pyngrok import ngrok

   # Set up ngrok
   public_url = ngrok.connect(port=8501)
   print(f"Public URL: {public_url}")

   # Change to the app directory
   os.chdir('sketch_to_krl')

   # Run the Streamlit app
   !streamlit run app.py &>/dev/null &

   # Keep the notebook running
   import IPython
   from IPython.display import display, HTML
   display(HTML(f"""
   <div style="background-color:#4CAF50; padding: 10px; border-radius: 5px;">
     <h3 style="color: white;">App is running!</h3>
     <p style="color: white;">Access your Sketch-to-KRL Code Generator at: <a href="{public_url}" target="_blank" style="color: white; text-decoration: underline;">{public_url}</a></p>
   </div>
   """))
   ```

3. Click on the generated URL to access the application

### 5. Using the Application

1. The application will open in a new browser tab
2. You can now use the Sketch-to-KRL Code Generator:
   - Upload or draw sketches
   - Configure robot path settings
   - Generate KRL code
   - Download the generated files

### 6. Important Notes

1. **Session Duration**: Google Colab sessions have a limited runtime (usually a few hours). After this period, you'll need to restart the notebook.

2. **Keeping the Session Alive**: To prevent the session from timing out:
   - Keep the Colab tab open
   - Periodically interact with the notebook
   - Consider using browser extensions that simulate activity

3. **Data Persistence**: Files created during a Colab session are temporary. To save your work:
   - Download important files before closing the session
   - Consider connecting Colab to Google Drive for persistent storage

4. **Resource Limits**: Google Colab has resource limitations. If you encounter performance issues:
   - Restart the runtime
   - Use smaller image files
   - Simplify complex paths

### 7. Creating Test Sketches

The notebook includes a section for creating test sketches. Run this cell to generate example sketches that you can use to test the application:

```python
# Create a simple test sketch
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# Create test sketches (square, circle, star, etc.)
# ...

# Display the test sketches
plt.figure(figsize=(15, 5))
# ...
plt.show()
```

## Troubleshooting

1. **Application Not Starting**:
   - Check for errors in the output of the cell that starts the Streamlit app
   - Ensure all required packages are installed
   - Restart the runtime and try again

2. **URL Not Working**:
   - Ngrok URLs expire after some time. Rerun the cell to get a new URL
   - Check if your network blocks ngrok connections

3. **File Upload Issues**:
   - Ensure the file is in a supported format (PNG, JPG)
   - Check if the file size is too large

4. **Path Extraction Problems**:
   - Use high-contrast sketches for better path detection
   - Try simplifying the sketch if complex paths are not detected correctly