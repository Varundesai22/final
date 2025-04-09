import streamlit as st

# --- Load Custom CSS ---
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
         pass # Assume loaded in app.py

load_css("style.css")

# --- Page Title ---
st.markdown("<h1>ℹ️ About PaveSafe.AI</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #FFD700;'>", unsafe_allow_html=True)

# --- Populate Content from your PDF Report ---
# Use st.markdown, st.write, st.expander etc.

st.markdown("## Project Overview")
st.markdown("""
**PaveSafe.AI** is an intelligent system developed by students at Pimpri Chinchwad College of Engineering (PCCOE), Pune.
Our goal is to automate the detection and classification of road surface defects like cracks and potholes using
state-of-the-art Deep Learning techniques. This project aims to improve road safety, optimize maintenance schedules,
and reduce the costs associated with manual road inspections.
""") # Replace with your Abstract/Introduction summary

st.markdown("## Problem Statement")
st.markdown("""
* Manual road inspection is time-consuming, subjective, and potentially hazardous.
* Delayed detection of potholes and cracks leads to further road degradation, increased vehicle damage, and higher accident risks.
* Lack of accurate, geo-tagged data hinders efficient resource allocation for road maintenance.
*(Expand or replace with details from your report)*
""")

st.markdown("## Proposed Solution & Methodology")
with st.expander("Click to view Methodology Details"):
    st.markdown("""
    1.  **Data Acquisition:** Collecting road surface images/videos using standard cameras or vehicle-mounted systems. *(Add details about your specific data collection)*
    2.  **Data Preprocessing:** Cleaning, resizing, and augmenting the dataset for model training. *(Specify your techniques)*
    3.  **Model Development:** Implementing a Deep Learning model (e.g., YOLO, Faster R-CNN, U-Net) trained to identify and classify defects. *(Mention your chosen model architecture)*
    4.  **Training & Validation:** Training the model on the prepared dataset and evaluating its performance using metrics like accuracy, precision, recall, and mAP. *(Include your performance results if available)*
    5.  **Deployment:** Integrating the trained model into this web application for real-time or batch analysis.
    6.  **GIS Integration (Optional):** Linking detected defects with GPS coordinates for mapping and analysis.
    *(Elaborate significantly based on your report)*
    """)

st.markdown("## Key Features")
st.markdown("""
* **Automated Detection:** Utilizes AI to automatically identify cracks and potholes from images/videos.
* **Defect Classification:** Differentiates between various types of defects (e.g., longitudinal cracks, transverse cracks, potholes).
* **Severity Estimation (Optional):** Provides an assessment of the severity level of detected defects. *(If implemented)*
* **User-Friendly Interface:** Simple web application for uploading media and viewing results.
* **Statistical Overview:** Provides a summary of detected defects and their locations (if available).
*(Add/modify based on your project's actual features)*
""")

st.markdown("## Technology Stack")
st.markdown("""
* **Programming Language:** Python
* **Deep Learning Framework:** [Your Framework, e.g., TensorFlow/Keras, PyTorch]
* **Web Framework:** Streamlit
* **Libraries:** Pandas, NumPy, OpenCV, Pillow, [Other relevant libraries]
*(List the specific tools you used)*
""")

st.markdown("## Development Team (PCCOE)")
st.markdown("""
* [Student Name 1] - [Role/Contribution]
* [Student Name 2] - [Role/Contribution]
* [Student Name 3] - [Role/Contribution]
* [Student Name 4] - [Role/Contribution]
* **Guide:** [Professor Name(s)]
*(List your team members and guide)*
""")

# --- Footer ---
st.markdown("---")
st.caption("© 2025 PaveSafe.AI | Pimpri Chinchwad College of Engineering, Pune")