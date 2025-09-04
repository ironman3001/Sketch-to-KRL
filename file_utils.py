import base64
import io
import zipfile
import streamlit as st

def get_download_link(file_content, file_name):
    """
    Create a download link for a text file
    
    Args:
        file_content: Content of the file as string
        file_name: Name of the file
        
    Returns:
        download_link: HTML link for downloading the file
    """
    b64 = base64.b64encode(file_content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{file_name}">Download {file_name}</a>'

def get_image_download_link(img, file_name):
    """
    Create a download link for an image
    
    Args:
        img: PIL Image object
        file_name: Name of the file
        
    Returns:
        download_link: HTML link for downloading the image
    """
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:file/png;base64,{img_str}" download="{file_name}">Download {file_name}</a>'

def create_zip_download(files_dict):
    """
    Create a download link for a zip file containing multiple files
    
    Args:
        files_dict: Dictionary of {filename: content}
        
    Returns:
        download_link: HTML link for downloading the zip file
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_name, file_content in files_dict.items():
            zip_file.writestr(file_name, file_content)
    
    zip_buffer.seek(0)
    b64 = base64.b64encode(zip_buffer.getvalue()).decode()
    
    return f'<a href="data:application/zip;base64,{b64}" download="krl_program.zip">Download All Files (ZIP)</a>'

def save_uploaded_file(uploaded_file):
    """
    Save an uploaded file to disk
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        file_path: Path to the saved file
    """
    import os
    
    # Create uploads directory if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    # Save the file
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path