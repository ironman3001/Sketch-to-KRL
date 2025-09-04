import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import cv2

def create_canvas():
    """
    Create a simple drawing canvas using Streamlit components
    Returns the drawn image as a numpy array
    """
    # Canvas state
    if 'canvas_image' not in st.session_state:
        # Create a blank white canvas
        st.session_state.canvas_image = Image.new('RGB', (500, 500), (255, 255, 255))
        st.session_state.canvas_draw = ImageDraw.Draw(st.session_state.canvas_image)
    
    # Display instructions
    st.markdown("### Drawing Canvas")
    st.markdown("Use the sliders below to draw lines on the canvas.")
    
    # Create columns for controls
    col1, col2 = st.columns(2)
    
    with col1:
        # Line start point
        start_x = st.slider("Start X", 0, 500, 100)
        start_y = st.slider("Start Y", 0, 500, 100)
    
    with col2:
        # Line end point
        end_x = st.slider("End X", 0, 500, 400)
        end_y = st.slider("End Y", 0, 500, 400)
    
    # Draw button
    if st.button("Draw Line"):
        # Draw a line on the canvas
        st.session_state.canvas_draw.line(
            [(start_x, start_y), (end_x, end_y)],
            fill=(0, 0, 0),
            width=5
        )
    
    # Clear button
    if st.button("Clear Canvas"):
        st.session_state.canvas_image = Image.new('RGB', (500, 500), (255, 255, 255))
        st.session_state.canvas_draw = ImageDraw.Draw(st.session_state.canvas_image)
    
    # Display the canvas
    st.image(st.session_state.canvas_image, caption="Drawing Canvas", use_column_width=True)
    
    # Convert to numpy array for OpenCV processing
    if st.button("Use This Drawing"):
        return np.array(st.session_state.canvas_image)
    
    return None