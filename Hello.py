import streamlit as st
import pandas as pd
import os
from datetime import datetime

def merge_csv_files(output_file, sellers_df, category_tree_df, csv_files):
    # Your existing merging logic here
    result_df = pd.DataFrame(columns=["SellerName", "SellerSku", "PrimaryCategory", "Name", "Brand"])

    # Merge all uploaded CSV files
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, delimiter=';', usecols=["SellerName", "SellerSku", "PrimaryCategory", "Name", "Brand"])
        result_df = pd.concat([result_df, df])

    # Call the function to merge the CSV files, perform VLOOKUP, and update PrimaryCategory
    # result_df = merge_csv_files(output_file, sellers_df, category_tree_df)

    return result_df

@st.cache(suppress_st_warning=True)
def load_cached_excel(file_uploader):
    if file_uploader:
        return pd.read_excel(file_uploader)
    return None

def main():
    st.title('CSV File Merger')
    
    # File uploader for Global*.csv files
    csv_files = st.file_uploader("Upload Global CSV Files", type=["csv"], accept_multiple_files=True)

    # Sellers and Category Tree file uploaders
    sellers_file = st.file_uploader("Upload Sellers Excel File", type=["xlsx"], key="sellers")
    category_tree_file = st.file_uploader("Upload Category Tree Excel File", type=["xlsx"], key="category_tree")

    # Load cached Excel files
    sellers_df = load_cached_excel(sellers_file)
    category_tree_df = load_cached_excel(category_tree_file)

    # Button to trigger the merging process
    if st.button("Merge CSV Files"):
        if csv_files and sellers_df is not None and category_tree_df is not None:
            # Specify the output file name
            output_file = "Merged_skus_date.csv"

            # Call the function to merge the CSV files, perform VLOOKUP, and update PrimaryCategory
            result_df = merge_csv_files(output_file, sellers_df, category_tree_df, csv_files)

            # Write result to a CSV file
            result_df.to_csv(output_file, index=False)
            st.success(f"CSV files merged successfully. Download the merged file from [here](./{output_file})")
        else:
            st.warning("Please upload all required files.")

if __name__ == "__main__":
    main()
