# Deploying to Hugging Face Spaces

This guide explains how to deploy the Sketch-to-KRL Code Generator application to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (sign up at [huggingface.co](https://huggingface.co) if you don't have one)
2. The complete Sketch-to-KRL Code Generator project files

## Deployment Steps

### 1. Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click on "Create new Space"
3. Fill in the following details:
   - **Owner**: Your username or organization
   - **Space name**: sketch-to-krl-generator (or any name you prefer)
   - **License**: Choose an appropriate license (e.g., MIT)
   - **SDK**: Select "Streamlit" from the dropdown
   - **Space hardware**: Choose "CPU" (the default option)
   - **Visibility**: Public or Private as per your preference

4. Click "Create Space"

### 2. Prepare Your Files

Ensure you have the following files ready for upload:

- `app.py`: Main Streamlit application
- `path_extraction.py`: Path extraction module
- `krl_generator.py`: KRL code generation module
- `drawing_canvas.py`: Drawing canvas component
- `path_visualization.py`: Path visualization utilities
- `file_utils.py`: File handling utilities
- `requirements.txt`: Required Python packages
- `README.md`: Project documentation

### 3. Upload Files to Hugging Face Spaces

You have two options for uploading files:

#### Option 1: Using the Web Interface

1. Go to your newly created Space
2. Click on "Files" tab
3. Click "Add file" and select "Upload files"
4. Upload all the required files mentioned above
5. Add a commit message and click "Commit changes to main"

#### Option 2: Using Git

1. Clone your Space repository:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/sketch-to-krl-generator
   ```

2. Copy all project files to the cloned directory:
   ```bash
   cp -r /path/to/your/project/* ./sketch-to-krl-generator/
   ```

3. Commit and push the changes:
   ```bash
   cd sketch-to-krl-generator
   git add .
   git commit -m "Initial commit of Sketch-to-KRL Code Generator"
   git push
   ```

### 4. Verify Deployment

1. After uploading all files, Hugging Face Spaces will automatically build and deploy your application
2. You can monitor the build process in the "Settings" tab under "Build logs"
3. Once the build is complete, your application will be available at:
   `https://huggingface.co/spaces/YOUR_USERNAME/sketch-to-krl-generator`

### 5. Troubleshooting

If your application fails to deploy, check the following:

1. **Build logs**: Check for any errors in the build process
2. **Requirements**: Ensure all required packages are listed in `requirements.txt`
3. **File structure**: Make sure all necessary files are uploaded
4. **Streamlit version**: Verify compatibility with the Streamlit version used by Hugging Face Spaces

### 6. Updating Your Application

To update your application after making changes:

1. Upload the modified files using the web interface or git
2. Hugging Face Spaces will automatically rebuild and redeploy your application

## Additional Resources

- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Streamlit Documentation](https://docs.streamlit.io/)