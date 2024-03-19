import streamlit as st
import pandas as pd
import os
from datetime import datetime

def merge_csv_files(sellers_df, category_tree_df, csv_files):
    # Your existing merging logic here
    result_df = pd.DataFrame(columns=["SellerName", "SellerSku", "PrimaryCategory", "Name", "Brand"])

    # Merge all uploaded CSV files
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, delimiter=';', usecols=["SellerName", "SellerSku", "PrimaryCategory", "Name", "Brand"])
        result_df = pd.concat([result_df, df])

    # Call the function to merge the CSV files, perform VLOOKUP, and update PrimaryCategory
    # result_df = merge_csv_files(output_file, sellers_df, category_tree_df)

    return result_df

def main():
    st.title('CSV File Merger')
    
    # File uploader for Global*.csv files
    csv_files = st.file_uploader("Upload Global CSV Files", type=["csv"], accept_multiple_files=True)

    # Check if sellers and category tree files exist in the script folder
    sellers_file_path = "sellers.xlsx"
    category_tree_file_path = "category_tree.xlsx"
    
    if os.path.exists(sellers_file_path) and os.path.exists(category_tree_file_path):
        sellers_df = pd.read_excel(sellers_file_path)
        category_tree_df = pd.read_excel(category_tree_file_path)
    else:
        sellers_df = None
        category_tree_df = None

    # Button to trigger the merging process
    if st.button("Merge CSV Files"):
        if csv_files and sellers_df is not None and category_tree_df is not None:
            # Specify the output file name
            output_file = "Merged_skus_date.csv"

            # Call the function to merge the CSV files, perform VLOOKUP, and update PrimaryCategory
            result_df = merge_csv_files(sellers_df, category_tree_df, csv_files)

            # Write result to a CSV file
            result_df.to_csv(output_file, index=False)

            # Generate a download link for the CSV file
            with open(output_file, "rb") as file:
                file_contents = file.read()
            st.download_button(label="Download Merged File", data=file_contents, file_name=output_file, mime="text/csv")
            
            st.success(f"CSV files merged successfully. Click the button above to download the merged file.")
        else:
            st.warning("Please upload all required files.")

if __name__ == "__main__":
    main()
