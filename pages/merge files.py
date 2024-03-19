import pandas as pd
import streamlit as st
from io import BytesIO
import base64

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
        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            # Check if the row is already in the merged DataFrame
            existing_row = merged_df[
                (merged_df == row).all(axis=1)
            ]  # Find rows that are identical
            if len(existing_row) == 0:
                # If the row is not in the merged DataFrame, append it
                merged_df = merged_df.append(row, ignore_index=True)
            else:
                # If the row is in the merged DataFrame, update only missing values
                existing_row_index = existing_row.index[0]
                merged_df.loc[existing_row_index] = merged_df.loc[
                    existing_row_index
                ].combine_first(row)

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
