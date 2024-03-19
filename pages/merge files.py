import pandas as pd
import streamlit as st
from io import BytesIO

def merge_excel_files(files):
    # Check if any files are provided
    if not files:
        st.error("No files provided.")
        return None
    
    # Initialize an empty DataFrame to store the merged data
    merged_df = pd.DataFrame()

    # Iterate through each file
    for file in files:
        # Read Excel file into a DataFrame
        df = pd.read_excel(file)
        # Merge the DataFrame
        merged_df = pd.concat([merged_df, df], ignore_index=True, sort=False)

    return merged_df

st.title("Excel Files Merger")

# Upload multiple files
uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    st.write("Files uploaded:")
    for file in uploaded_files:
        st.write(file.name)

    # Merge files and display progress
    merged_df = merge_excel_files(uploaded_files)
    
    if merged_df is not None:
        st.success("Files merged successfully!")

        # Download merged file
        csv = merged_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="merged_output.csv">Download Merged File</a>'
        st.markdown(href, unsafe_allow_html=True)
