import streamlit as st
import pandas as pd
import os
import gdown  # for downloading files from Google Drive
from datetime import datetime

def download_file(url, output_path):
    """
    Downloads a file from the given URL to the specified output path.
    """
    with st.spinner("Downloading file..."):
        gdown.download(url, output_path, quiet=False)

def merge_csv_files(output_file, sellers_df, category_tree_df, csv_files):
    # Your existing merging logic here
    result_df = pd.DataFrame(columns=["SellerName", "SellerSku", "PrimaryCategory", "Name", "Brand"])

    # Merge all uploaded CSV files
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, delimiter=';', usecols=["SellerName", "SellerSku", "PrimaryCategory", "Name", "Brand"])
        result_df = pd.concat([result_df, df])

    # Call the function to merge the CSV files, perform VLOOKUP, and update PrimaryCategory
    result_df = merge_csv_files(output_file, sellers_df, category_tree_df)

    return result_df

def main():
    st.title('CSV File Merger')
    
    # File uploader for Global*.csv files
    csv_files = st.file_uploader("Upload Global CSV Files", type=["csv"], accept_multiple_files=True)

    # Check if the sellers and category tree files are already downloaded
    sellers_file_path = "sellers.xlsx"
    category_tree_file_path = "category_tree.xlsx"

    if not os.path.exists(sellers_file_path):
        st.warning("Sellers Excel file not found. Please upload or provide the link.")
        sellers_url = st.text_input("Enter the link to the Sellers Excel file:")
        if sellers_url:
            download_file(sellers_url, sellers_file_path)
    else:
        st.success("Sellers Excel file found.")

    if not os.path.exists(category_tree_file_path):
        st.warning("Category Tree Excel file not found. Please upload or provide the link.")
        category_tree_url = st.text_input("Enter the link to the Category Tree Excel file:")
        if category_tree_url:
            download_file(category_tree_url, category_tree_file_path)
    else:
        st.success("Category Tree Excel file found.")

    # Button to trigger the merging process
    if st.button("Merge CSV Files"):
        if csv_files:
            sellers_df = pd.read_excel(sellers_file_path)
            category_tree_df = pd.read_excel(category_tree_file_path)

            # Specify the output file name
            output_file = "Merged_skus_date.csv"

            # Call the function to merge the CSV files, perform VLOOKUP, and update PrimaryCategory
            result_df = merge_csv_files(output_file, sellers_df, category_tree_df, csv_files)

            # Write result to a CSV file
            result_df.to_csv(output_file, index=False)
            st.success(f"CSV files merged successfully. Download the merged file from [here](./{output_file})")
        else:
            st.warning("Please upload at least one CSV file.")

if __name__ == "__main__":
    main()
