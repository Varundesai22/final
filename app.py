import streamlit as st
from PIL import Image
import pandas as pd
import os
import time # For simulation
from model_utils import load_detection_model, run_detection_on_image, run_detection_on_video # Import your functions

# --- Page Configuration ---
st.set_page_config(
    page_title="PaveSafe.AI",
    page_icon="assets/pavesafe_logo.jpg", # Favicon
    layout="wide", # Use wide layout
    initial_sidebar_state="expanded" # Keep sidebar open initially
)

# --- Load Custom CSS ---
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}")

load_css("style.css")

# --- Logo Display ---
# Use columns to control layout/centering if needed, or use the CSS class
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
try:
    logo_pavesafe = Image.open("assets/pavesafe_logo.jpg")
    logo_pccoe = Image.open("assets/pccoe_logo.png")
    # Apply CSS class directly if possible, otherwise use columns
    col1, col2, col3 = st.columns([1,0.5,1]) # Adjust ratios as needed
    with col1:
        st.write("") # Spacer
    with col2:
         st.image(logo_pavesafe, width=120) # Adjust width
         st.image(logo_pccoe, width=120) # Adjust width
    with col3:
        st.write("") # Spacer

    # Alternative using markdown class (if CSS targets stImage within the class)
    # st.image(logo_pavesafe, width=80) # Adjust width
    # st.image(logo_pccoe, width=150) # Adjust width

except FileNotFoundError:
    st.error("Logo file(s) not found in 'assets' folder. Please ensure 'pavesafe_logo.jpg' and 'pccoe_logo.png' exist.")
st.markdown('</div>', unsafe_allow_html=True)


# --- Page Title ---
st.markdown("<h1>Welcome to PaveSafe.AI</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #FFD700;'>", unsafe_allow_html=True) # Thematic separator

# --- Main Content ---
st.markdown("## Upload Road Image or Video for Analysis")
st.markdown("""
Upload an image or a video file containing road surfaces. Our AI model, developed at
Pimpri Chinchwad College of Engineering, will analyze it to detect and classify
potential cracks and potholes.
""")

# --- File Uploader ---
uploaded_file = st.file_uploader(
    "Choose an image or video file",
    type=["jpg", "jpeg", "png", "bmp", "mp4", "avi", "mov"],
    accept_multiple_files=False,
    key="file_uploader"
)

# --- Analysis Section ---
if uploaded_file is not None:
    file_type = uploaded_file.type
    file_size = uploaded_file.size

    st.markdown("---")
    st.markdown("### Uploaded File Preview & Analysis")

    # Display file details
    st.write(f"**File Name:** {uploaded_file.name}")
    st.write(f"**File Type:** {file_type}")
    st.write(f"**File Size:** {file_size / (1024*1024):.2f} MB")

    col1, col2 = st.columns([1, 1]) # Create two columns for preview and results

    analysis_placeholder = st.empty() # Placeholder for status updates/results

    # --- Trigger Analysis ---
    if st.button("Analyze File", key="analyze_button"):
        model = load_detection_model() # Load the model (cached)
        if model is None:
             analysis_placeholder.error("❌ Model could not be loaded. Cannot perform analysis.")
        else:
            with analysis_placeholder.container():
                with st.spinner('⚙️ Analyzing... Please wait.'):
                    if file_type.startswith('image/'):
                        # --- Image Analysis ---
                        image_bytes = uploaded_file.getvalue()
                        with col1:
                             st.image(image_bytes, caption="Uploaded Image", use_column_width=True)

                        # Run detection (replace with your actual function call)
                        results = run_detection_on_image(model, image_bytes)

                        with col2:
                            if results and results.get('detections') is not None:
                                st.success("✅ Analysis Complete!")
                                st.markdown("#### Detection Results:")
                                detections = results['detections']
                                if detections:
                                    df_results = pd.DataFrame(detections)
                                    st.dataframe(df_results[['label', 'confidence', 'box']]) # Show basic results
                                    # Display processed image if available
                                    if results.get('processed_image'):
                                        st.image(results['processed_image'], caption="Processed Image with Detections", use_column_width=True)
                                else:
                                    st.info("ℹ️ No defects detected in the image.")
                            else:
                                st.error("❌ Analysis failed or returned no results.")

                    elif file_type.startswith('video/'):
                        # --- Video Analysis ---
                        with col1:
                            st.video(uploaded_file)

                        # Save video temporarily to process with libraries like OpenCV
                        temp_dir = "temp_video_files"
                        os.makedirs(temp_dir, exist_ok=True)
                        temp_video_path = os.path.join(temp_dir, uploaded_file.name)

                        try:
                            with open(temp_video_path, "wb") as f:
                                f.write(uploaded_file.getvalue())

                            # Run detection (replace with your actual function call)
                            results = run_detection_on_video(model, temp_video_path)

                            with col2:
                                if results:
                                    st.success("✅ Video Analysis Complete!")
                                    st.markdown("#### Detection Summary:")
                                    st.metric("Total Potholes Found", results.get('total_potholes', 'N/A'))
                                    st.metric("Total Cracks Found", results.get('total_cracks', 'N/A'))
                                    # Optionally provide download link for processed video if created
                                    # if results.get('processed_video_path'):
                                    #     st.download_button(...)
                                else:
                                    st.error("❌ Video analysis failed.")

                        except Exception as e:
                            with col2:
                                st.error(f"❌ Error processing video: {e}")
                        finally:
                            # Clean up temporary file
                            if os.path.exists(temp_video_path):
                                os.remove(temp_video_path)
                                print(f"Removed temp file: {temp_video_path}")

                    else:
                         analysis_placeholder.warning("⚠️ Unsupported file type for analysis.")

    # Show initial preview if button not clicked yet
    elif file_type.startswith('image/'):
         with col1:
            st.image(uploaded_file.getvalue(), caption="Uploaded Image Preview", use_column_width=True)
         with col2:
             st.info("Click 'Analyze File' to process the image.")
    elif file_type.startswith('video/'):
        with col1:
            st.video(uploaded_file)
        with col2:
             st.info("Click 'Analyze File' to process the video.")

else:
    st.info("👆 Upload a file using the uploader above to get started.")

# --- Footer ---
st.markdown("---")
st.caption("© 2025 PaveSafe.AI | Developed by PCCOE Students")