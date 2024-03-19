import pandas as pd
import streamlit as st
from io import BytesIO
import base64

def merge_excel_files(files):
    # Check if any files are provided
    if not files:
        st.error("No files provided.")
        return None
    
    # Initialize an empty list to store DataFrames
    dfs = []
    sheet_names = set()

    # Iterate through each file
    for file in files:
        # Read Excel file into a dictionary of DataFrames (one DataFrame per sheet)
        xls = pd.ExcelFile(file)
        # Get sheet names
        file_sheet_names = xls.sheet_names
        # Ensure all files have the same set of sheet names
        if not sheet_names:
            sheet_names.update(file_sheet_names)
        elif sheet_names != set(file_sheet_names):
            st.error("Sheet names are not consistent across all files.")
            return None

        # Iterate through each sheet
        for sheet_name in file_sheet_names:
            # Read the sheet into a DataFrame
            df = pd.read_excel(file, sheet_name=sheet_name)
            # Add filename and sheet name as a prefix to each column name to differentiate columns from different files
            df.columns = [f"{file}_{sheet_name}_{col}" for col in df.columns]
            dfs.append(df)

    # Concatenate all DataFrames
    merged_df = pd.concat(dfs, axis=1)

    # Drop duplicate columns
    merged_df = merged_df.loc[:,~merged_df.columns.duplicated()]

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
