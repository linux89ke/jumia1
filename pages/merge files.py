import pandas as pd
import streamlit as st
import base64

def preprocess_data(df):
    # Check if 'Categories' column exists in the DataFrame
    if 'Categories' in df.columns:
        # Split the 'Categories' column into 'ID' and 'Full Value'
        df[['ID', 'Full Value']] = df['Categories'].str.split(' - ', 1, expand=True)
        # Split the 'Full Value' column into individual categories
        df['Categories'] = df['Full Value'].str.split(' / ')
        # Fill missing values with empty lists
        df['Categories'] = df['Categories'].fillna('').astype(str)
    else:
        # If 'Categories' column is not present, create dummy columns
        df['ID'] = ""
        df['Full Value'] = ""
        df['Categories'] = ""
    return df

def merge_excel_files(files):
    # Check if any files are provided
    if not files:
        st.error("No files provided.")
        return None
    
    # Initialize an empty list to store DataFrames
    dfs = []

    # Iterate through each file
    for file in files:
        # Read Excel file into a DataFrame
        xls = pd.ExcelFile(file)
        # Check if the sheet "Categories" exists in the file
        if "Categories" in xls.sheet_names:
            # Read the sheet into a DataFrame
            df = pd.read_excel(file, sheet_name="Categories")
            # Preprocess the data to split categories into separate columns
            df = preprocess_data(df)
            # Add filename as a prefix to each column name to differentiate columns from different files
            df.columns = [f"{file}_{col}" for col in df.columns]
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
        
        # Checkbox to trigger download
        if st.checkbox("Download Merged Output"):
            # Download merged file
            csv = merged_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="merged_output.csv">Download Merged File</a>'
            st.markdown(href, unsafe_allow_html=True)
