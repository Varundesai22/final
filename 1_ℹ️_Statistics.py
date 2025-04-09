import streamlit as st
import pandas as pd
import os

# --- Load Custom CSS ---
# You might need to reload CSS on each page if Streamlit doesn't persist it perfectly across pages
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
         # Don't show error on subpages, assume it loaded in app.py
         pass

load_css("style.css") # Use relative path

# --- Page Title ---
st.markdown("<h1>📊 Detection Statistics</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #FFD700;'>", unsafe_allow_html=True)

st.markdown("## View Recorded Detection Data")
st.markdown("""
This page displays the aggregated detection data, including coordinates and severity,
logged during analysis sessions. The data is presented in a table format below.
You can sort columns by clicking on their headers.
*(Note: This currently displays sample static data)*
""")

# --- Load Data ---
CSV_FILE_PATH = os.path.join("data", "detection_stats.csv")

try:
    df = pd.read_csv(CSV_FILE_PATH)

    # Optional: Data Cleaning / Type Conversion
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    numeric_cols = ['Latitude', 'Longitude', 'Severity']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # --- Display Data Table ---
    st.markdown("### Detection Log")

    # Use st.data_editor for an Excel-like view (allows editing if not disabled)
    # st.data_editor(df, use_container_width=True, num_rows="dynamic", disabled=True) # disabled=True makes it view-only

    # Use st.dataframe for a standard view
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # --- Basic Statistics & Map ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Summary Statistics")
        if not df.empty:
            # Display some metrics
            total_detections = len(df)
            pothole_count = df[df['Defect_Type'].str.contains("pothole", case=False, na=False)].shape[0] if 'Defect_Type' in df.columns else 'N/A'
            crack_count = df[df['Defect_Type'].str.contains("crack", case=False, na=False)].shape[0] if 'Defect_Type' in df.columns else 'N/A'

            st.metric("Total Detections Logged", total_detections)
            st.metric("Potholes Logged", pothole_count)
            st.metric("Cracks Logged", crack_count)

            # Show describe() output in an expander
            with st.expander("Detailed Numeric Stats"):
                st.dataframe(df.describe())
        else:
            st.info("No data available to calculate statistics.")

    with col2:
        st.markdown("### Detection Locations Map")
        # Check if necessary columns exist and have valid data
        if 'Latitude' in df.columns and 'Longitude' in df.columns and not df[['Latitude', 'Longitude']].isnull().all().all():
             map_df = df[['Latitude', 'Longitude']].dropna()
             if not map_df.empty:
                st.map(map_df, zoom=11) # Adjust zoom level as needed
             else:
                st.info("No valid coordinates found in the data to display on map.")
        else:
            st.info("Coordinate data (Latitude, Longitude columns) not found or is invalid.")


except FileNotFoundError:
    st.error(f"❌ Statistics file not found at '{CSV_FILE_PATH}'. Please ensure 'data/detection_stats.csv' exists.")
except pd.errors.EmptyDataError:
     st.warning(f"⚠️ The statistics file '{CSV_FILE_PATH}' is empty.")
except Exception as e:
    st.error(f"❌ An error occurred while loading or processing the statistics data: {e}")

# --- Footer ---
st.markdown("---")
st.caption("© 2025 PaveSafe.AI | Developed by PCCOE Students")