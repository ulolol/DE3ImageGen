import requests
import streamlit as st
import openai
import os
from PIL import Image
import io
import toml

# Load API key from configuration file
config_file = "SearchShellGPT.toml"
if os.path.exists(config_file):
    config = toml.load(config_file)
    api_key = config["openai"]["api_key"]
else:
    api_key = None

# Page configuration
st.set_page_config(page_title="DALL-E 3 Image Generator", page_icon=":art:", layout="wide")

# Title and description
st.title("🎨 DALL-E 3 Image Gen")
st.write("Generate images using DALL-E 3 API")

# Sidebar for API configuration
st.sidebar.header("OpenAI API Config")
if api_key:
    st.sidebar.write(f"API Key (from {config_file}): `API_KEY_LOADED_FROM_FILE`")
else:
    api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Image generation options
st.sidebar.header("Image Gen Settings")
image_size_options = ["1024x1024", "1024x1792", "1792x1024"]
image_size = st.sidebar.selectbox("Select Image Size", image_size_options, index=0)

#num_images = st.sidebar.slider("Number of Images to Generate", 1, 10, 1)

# Quality options
quality_options = ["standard", "hd"]
image_quality = st.sidebar.selectbox("Image Quality", quality_options, index=0)

# Style options
style_options = ["vivid", "natural"]
image_style = st.sidebar.selectbox("Image Style", style_options, index=0)

# Main input for prompt
prompt = st.text_area("Enter your image generation prompt", 
                      placeholder="The word `Ka0$` written across the canvas diagonally in a fluid style")

# Generate button
generate_button = st.button("Generate Images")

def generate_images(api_key, prompt, size, quality, style):
    """Generate images using DALL-E 3 API"""
    try:
        # Set up the OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Generate images
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            style=style,
            #n=num_images
        )
        
        return response
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Image generation logic
if generate_button:
    # Validate inputs
    if not api_key:
        st.warning("Make sure API key TOML exists, or enter API Key manually!")
    elif not prompt:
        st.warning("Please enter a prompt for image generation")
    else:
        # Show loading spinner
        with st.spinner("Generating images..."):
            # Set OpenAI API key
            openai.api_key = api_key
            
            # Generate images
            response = generate_images(api_key, prompt, image_size, image_quality, image_style)
            
            # Display generated images
            if response:
                st.success(f"Generated image!")
                
                # Create columns for images
                #cols = st.columns(num_images)
                cols = st.columns(1)
                
                for i, image_data in enumerate(response.data):
                    with cols[i]:
                        st.image(image_data.url)
                        
                        # Download button for each image
                        image_bytes = requests.get(image_data.url).content
                        st.download_button(
                            label=f"Download Image {i+1}",
                            data=image_bytes,
                            file_name=f"dalle_image_{i+1}.png",
                            mime="image/png"
                        )

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
    ### Usage Instructions:
    1. Ensure your API Key is present in the 'SearchShellGPT.toml' file or enter it manually
    2. Write a detailed prompt
    3. Adjust image settings
    4. Click 'Generate Images'
""")
