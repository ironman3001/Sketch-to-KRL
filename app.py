import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io
import base64
import os

# Import custom modules
from path_extraction import extract_paths_from_sketch, visualize_paths
from krl_generator import KRLGenerator
from file_utils import get_download_link, create_zip_download
from drawing_canvas import DrawingCanvas
from path_visualization import visualize_robot_path, get_visualization_as_image, overlay_path_on_image

# Set page configuration
st.set_page_config(
    page_title="Sketch-to-KRL Code Generator",
    page_icon="🤖",
    layout="wide"
)

# App title and description
st.title("Sketch-to-KRL Code Generator")
st.markdown("""
Upload or draw a sketch of robot paths, and this app will help you generate KUKA Robot Language (KRL) code.
""")

# Global variables to store app state
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'extracted_paths' not in st.session_state:
    st.session_state.extracted_paths = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = "upload"  # Possible values: upload, qa, generate, output
if 'start_position' not in st.session_state:
    st.session_state.start_position = "HOME"
if 'motion_types' not in st.session_state:
    st.session_state.motion_types = ["LIN"]
if 'use_coordinates' not in st.session_state:
    st.session_state.use_coordinates = False
if 'krl_code' not in st.session_state:
    st.session_state.krl_code = ""
if 'dat_code' not in st.session_state:
    st.session_state.dat_code = ""
if 'path_smoothing' not in st.session_state:
    st.session_state.path_smoothing = False
if 'extract_dimensions' not in st.session_state:
    st.session_state.extract_dimensions = False
if 'path_simplification' not in st.session_state:
    st.session_state.path_simplification = 50
if 'original_image' not in st.session_state:
    st.session_state.original_image = None

# Function to reset app state
def reset_app():
    st.session_state.processed_image = None
    st.session_state.extracted_paths = None
    st.session_state.current_step = "upload"
    st.session_state.start_position = "HOME"
    st.session_state.motion_types = ["LIN"]
    st.session_state.use_coordinates = False
    st.session_state.krl_code = ""
    st.session_state.dat_code = ""
    st.session_state.path_smoothing = False
    st.session_state.extract_dimensions = False
    st.session_state.path_simplification = 50
    st.session_state.original_image = None

# Main app logic based on current step
if st.session_state.current_step == "upload":
    # Create two columns for upload and drawing options
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Upload Sketch")
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Read and process the uploaded image
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            # Store original image
            st.session_state.original_image = image.copy()
            
            # Process the sketch
            processed_image, paths = extract_paths_from_sketch(image)
            
            # Store in session state
            st.session_state.processed_image = processed_image
            st.session_state.extracted_paths = paths
            
            # Display the processed image
            st.image(processed_image, caption="Processed Sketch", use_column_width=True)
            
            # Move to the next step
            if st.button("Continue with this sketch"):
                st.session_state.current_step = "qa"
                st.experimental_rerun()
    
    with col2:
        st.header("Draw Sketch")
        
        # Create drawing canvas
        canvas = DrawingCanvas(width=500, height=500)
        drawn_image = canvas.render()
        
        if drawn_image is not None:
            # Store original image
            st.session_state.original_image = drawn_image.copy()
            
            # Process the drawn image
            processed_image, paths = extract_paths_from_sketch(drawn_image)
            
            # Store in session state
            st.session_state.processed_image = processed_image
            st.session_state.extracted_paths = paths
            
            # Move to the next step
            st.session_state.current_step = "qa"
            st.experimental_rerun()

elif st.session_state.current_step == "qa":
    # Display the processed image
    if st.session_state.processed_image is not None:
        st.image(st.session_state.processed_image, caption="Processed Sketch", width=400)
    
    # Q&A section
    st.header("Configure Robot Path")
    
    # Start position
    st.session_state.start_position = st.radio(
        "Select start position:",
        ["HOME", "Anywhere"]
    )
    
    # Motion types
    motion_options = st.multiselect(
        "Select motion type(s):",
        ["LIN", "PTP", "CIRC", "SPLINE"],
        default=["LIN"]
    )
    
    if motion_options:
        st.session_state.motion_types = motion_options
    
    # Use coordinates
    st.session_state.use_coordinates = st.checkbox(
        "Use exact coordinates from sketch",
        value=False
    )
    
    # Additional clarifications
    with st.expander("Additional Options"):
        st.session_state.path_smoothing = st.checkbox("Enable path smoothing", value=False)
        st.session_state.extract_dimensions = st.checkbox("Extract dimensions from sketch", value=False)
        st.session_state.path_simplification = st.slider("Path simplification", 0, 100, 50)
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Upload"):
            st.session_state.current_step = "upload"
            st.experimental_rerun()
    with col2:
        if st.button("Generate KRL Code"):
            # Create KRL generator
            krl_gen = KRLGenerator()
            
            # Generate KRL code
            src_code = krl_gen.generate_src_code(
                st.session_state.extracted_paths,
                st.session_state.start_position,
                st.session_state.motion_types,
                st.session_state.use_coordinates
            )
            
            # Generate DAT code
            dat_code = krl_gen.generate_dat_code(st.session_state.use_coordinates)
            
            # Store in session state
            st.session_state.krl_code = src_code
            st.session_state.dat_code = dat_code
            
            # Move to output step
            st.session_state.current_step = "output"
            st.experimental_rerun()

elif st.session_state.current_step == "output":
    # Create columns for visualization and code
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Path Visualization")
        
        # Create tabs for different visualizations
        viz_tab1, viz_tab2 = st.tabs(["2D Path", "Overlay on Sketch"])
        
        with viz_tab1:
            # Create 2D visualization
            if st.session_state.extracted_paths:
                fig = visualize_robot_path(
                    st.session_state.extracted_paths,
                    st.session_state.motion_types
                )
                st.pyplot(fig)
        
        with viz_tab2:
            # Create overlay visualization
            if st.session_state.original_image is not None and st.session_state.extracted_paths:
                overlay_image = overlay_path_on_image(
                    st.session_state.original_image,
                    st.session_state.extracted_paths,
                    st.session_state.motion_types
                )
                st.image(overlay_image, caption="Path Overlay on Original Sketch", use_column_width=True)
    
    with col2:
        st.header("Generated KRL Code")
        
        # Create tabs for SRC and DAT files
        code_tab1, code_tab2 = st.tabs(["SRC File", "DAT File"])
        
        with code_tab1:
            st.code(st.session_state.krl_code, language="kotlin")
        
        with code_tab2:
            st.code(st.session_state.dat_code, language="kotlin")
        
        # Download options
        st.subheader("Download Files")
        
        # Create download links
        files_dict = {
            "PATH_PROGRAM.src": st.session_state.krl_code,
            "PATH_PROGRAM.dat": st.session_state.dat_code
        }
        
        # Individual file downloads
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(get_download_link(st.session_state.krl_code, "PATH_PROGRAM.src"), unsafe_allow_html=True)
        with col2:
            st.markdown(get_download_link(st.session_state.dat_code, "PATH_PROGRAM.dat"), unsafe_allow_html=True)
        
        # ZIP download
        st.markdown(create_zip_download(files_dict), unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Configuration"):
            st.session_state.current_step = "qa"
            st.experimental_rerun()
    with col2:
        if st.button("Start Over"):
            reset_app()
            st.experimental_rerun()

# Add a sidebar with information
with st.sidebar:
    st.header("About")
    st.info("""
    This app converts sketches into KUKA Robot Language (KRL) code.
    
    **Steps:**
    1. Upload or draw a sketch
    2. Configure robot path settings
    3. Generate and download KRL code
    
    **Supported Motion Types:**
    - LIN: Linear motion
    - PTP: Point-to-Point motion
    - CIRC: Circular motion
    - SPLINE: Spline motion
    """)
    
    # Add information about KRL
    with st.expander("About KUKA Robot Language"):
        st.markdown("""
        **KUKA Robot Language (KRL)** is the programming language used for KUKA industrial robots.
        
        **Key Components:**
        - **.src files**: Contain the program logic and motion commands
        - **.dat files**: Contain point definitions and other data
        
        **Common Motion Commands:**
        - **PTP**: Point-to-Point motion (fastest path)
        - **LIN**: Linear motion (straight line)
        - **CIRC**: Circular motion (requires auxiliary point)
        - **SPLINE**: Smooth curved motion
        
        **Example KRL Program:**
        ```
        DEF EXAMPLE()
           BAS (#INITMOV,0)
           PTP HOME
           LIN P1
           CIRC P2, P3
           PTP HOME
        END
        ```
        """)
    
    # Add a reset button
    if st.button("Reset Application"):
        reset_app()
        st.experimental_rerun()