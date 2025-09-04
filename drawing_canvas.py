import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import cv2
import base64
from io import BytesIO

class DrawingCanvas:
    """
    Interactive drawing canvas for Streamlit
    """
    
    def __init__(self, width=500, height=500, background_color=(255, 255, 255)):
        """
        Initialize the drawing canvas
        
        Args:
            width: Canvas width in pixels
            height: Canvas height in pixels
            background_color: Canvas background color as RGB tuple
        """
        self.width = width
        self.height = height
        self.background_color = background_color
        
        # Initialize canvas state if not already in session state
        if 'canvas_image' not in st.session_state:
            self.reset_canvas()
        
        if 'drawing_mode' not in st.session_state:
            st.session_state.drawing_mode = "line"
        
        if 'drawing_color' not in st.session_state:
            st.session_state.drawing_color = (0, 0, 0)
        
        if 'drawing_thickness' not in st.session_state:
            st.session_state.drawing_thickness = 3
        
        if 'drawing_points' not in st.session_state:
            st.session_state.drawing_points = []
    
    def reset_canvas(self):
        """Reset the canvas to a blank state"""
        st.session_state.canvas_image = Image.new('RGB', (self.width, self.height), self.background_color)
        st.session_state.canvas_draw = ImageDraw.Draw(st.session_state.canvas_image)
        st.session_state.drawing_points = []
    
    def render(self):
        """
        Render the drawing canvas in the Streamlit app
        
        Returns:
            image: The drawn image as numpy array if submitted, None otherwise
        """
        st.markdown("### Drawing Canvas")
        st.markdown("Draw your robot path on the canvas below.")
        
        # Drawing tools
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.session_state.drawing_mode = st.selectbox(
                "Drawing Mode",
                ["line", "rectangle", "circle", "freehand"]
            )
        
        with col2:
            color_options = {
                "Black": (0, 0, 0),
                "Red": (255, 0, 0),
                "Green": (0, 255, 0),
                "Blue": (0, 0, 255)
            }
            color_choice = st.selectbox("Color", list(color_options.keys()))
            st.session_state.drawing_color = color_options[color_choice]
        
        with col3:
            st.session_state.drawing_thickness = st.slider("Thickness", 1, 10, 3)
        
        # Canvas area
        canvas_col, controls_col = st.columns([3, 1])
        
        with canvas_col:
            # Display the canvas
            st.image(st.session_state.canvas_image, caption="Drawing Canvas", use_column_width=True)
            
            # Create a placeholder for the canvas
            canvas_placeholder = st.empty()
            
            # Display the current canvas
            canvas_placeholder.image(st.session_state.canvas_image, caption="Drawing Canvas", use_column_width=True)
        
        with controls_col:
            # Drawing controls based on mode
            if st.session_state.drawing_mode == "line":
                st.markdown("#### Draw Line")
                start_x = st.slider("Start X", 0, self.width, self.width // 4)
                start_y = st.slider("Start Y", 0, self.height, self.height // 4)
                end_x = st.slider("End X", 0, self.width, 3 * self.width // 4)
                end_y = st.slider("End Y", 0, self.height, 3 * self.height // 4)
                
                if st.button("Add Line"):
                    st.session_state.canvas_draw.line(
                        [(start_x, start_y), (end_x, end_y)],
                        fill=st.session_state.drawing_color,
                        width=st.session_state.drawing_thickness
                    )
                    # Add points to the drawing points list
                    st.session_state.drawing_points.append((start_x, start_y))
                    st.session_state.drawing_points.append((end_x, end_y))
                    # Update the canvas display
                    canvas_placeholder.image(st.session_state.canvas_image, caption="Drawing Canvas", use_column_width=True)
            
            elif st.session_state.drawing_mode == "rectangle":
                st.markdown("#### Draw Rectangle")
                start_x = st.slider("Left", 0, self.width, self.width // 4)
                start_y = st.slider("Top", 0, self.height, self.height // 4)
                end_x = st.slider("Right", 0, self.width, 3 * self.width // 4)
                end_y = st.slider("Bottom", 0, self.height, 3 * self.height // 4)
                
                if st.button("Add Rectangle"):
                    st.session_state.canvas_draw.rectangle(
                        [(start_x, start_y), (end_x, end_y)],
                        outline=st.session_state.drawing_color,
                        width=st.session_state.drawing_thickness
                    )
                    # Add points to the drawing points list (corners of rectangle)
                    st.session_state.drawing_points.extend([
                        (start_x, start_y),
                        (end_x, start_y),
                        (end_x, end_y),
                        (start_x, end_y),
                        (start_x, start_y)  # Close the rectangle
                    ])
                    # Update the canvas display
                    canvas_placeholder.image(st.session_state.canvas_image, caption="Drawing Canvas", use_column_width=True)
            
            elif st.session_state.drawing_mode == "circle":
                st.markdown("#### Draw Circle")
                center_x = st.slider("Center X", 0, self.width, self.width // 2)
                center_y = st.slider("Center Y", 0, self.height, self.height // 2)
                radius = st.slider("Radius", 5, min(self.width, self.height) // 2, 50)
                
                if st.button("Add Circle"):
                    st.session_state.canvas_draw.ellipse(
                        [(center_x - radius, center_y - radius), 
                         (center_x + radius, center_y + radius)],
                        outline=st.session_state.drawing_color,
                        width=st.session_state.drawing_thickness
                    )
                    # Add points approximating a circle
                    num_points = 20
                    for i in range(num_points + 1):
                        angle = 2 * np.pi * i / num_points
                        x = center_x + radius * np.cos(angle)
                        y = center_y + radius * np.sin(angle)
                        st.session_state.drawing_points.append((int(x), int(y)))
                    # Update the canvas display
                    canvas_placeholder.image(st.session_state.canvas_image, caption="Drawing Canvas", use_column_width=True)
            
            elif st.session_state.drawing_mode == "freehand":
                st.markdown("#### Freehand Drawing")
                st.markdown("Coming soon: Interactive freehand drawing")
                st.markdown("For now, use the other drawing modes.")
            
            # Clear button
            if st.button("Clear Canvas"):
                self.reset_canvas()
                canvas_placeholder.image(st.session_state.canvas_image, caption="Drawing Canvas", use_column_width=True)
        
        # Submit button
        if st.button("Use This Drawing"):
            # Convert to numpy array for OpenCV processing
            return np.array(st.session_state.canvas_image)
        
        return None
    
    def get_drawing_points(self):
        """
        Get the points that were drawn on the canvas
        
        Returns:
            points: List of (x, y) coordinate tuples
        """
        return st.session_state.drawing_points
    
    def get_image_as_base64(self):
        """
        Get the canvas image as a base64 encoded string
        
        Returns:
            base64_image: Base64 encoded image string
        """
        buffered = BytesIO()
        st.session_state.canvas_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str