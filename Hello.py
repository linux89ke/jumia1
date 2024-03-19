import streamlit as st
import pandas as pd
import os
from datetime import datetime

@st.cache(allow_output_mutation=True)
def load_data(file):
    return pd.read_excel(file)

def merge_csv_files(output_file, sellers_df, category_tree_df):
    # Your existing merging logic here

    # Return the merged DataFrame
    return result_df

def main():
    st.title('CSV File Merger')
    
    # File uploader for Global*.csv files
    csv_files = st.file_uploader("Upload Global CSV Files", type=["csv"], accept_multiple_files=True)

    # File uploader for sellers.xlsx
    sellers_file = st.file_uploader("Upload Sellers Excel File", type=["xlsx"])

    # File uploader for category_tree.xlsx
    category_tree_file = st.file_uploader("Upload Category Tree Excel File", type=["xlsx"])

    # Load or cache sellers and category tree files
    if sellers_file is not None:
        sellers_df = load_data(sellers_file)
    else:
        st.warning("Please upload sellers.xlsx file.")

    if category_tree_file is not None:
        category_tree_df = load_data(category_tree_file)
    else:
        st.warning("Please upload category_tree.xlsx file.")

    # Button to trigger the merging process
    if st.button("Merge CSV Files"):
        if sellers_file is not None and category_tree_file is not None:
            # Check if at least one CSV file is uploaded
            if csv_files:
                result_df = pd.DataFrame(columns=["SellerName", "SellerSku", "PrimaryCategory", "Name", "Brand"])

                # Merge all uploaded CSV files
                for csv_file in csv_files:
                    df = pd.read_csv(csv_file, delimiter=';', usecols=["SellerName", "SellerSku", "PrimaryCategory", "Name", "Brand"])
                    result_df = pd.concat([result_df, df])

                # Specify the output file name
                output_file = "Merged_skus_date.csv"

                # Call the function to merge the CSV files, perform VLOOKUP, and update PrimaryCategory
                result_df = merge_csv_files(output_file, sellers_df, category_tree_df)

                # Write result to a CSV file
                result_df.to_csv(output_file, index=False)
                st.success(f"CSV files merged successfully. Download the merged file from [here](./{output_file})")
            else:
                st.warning("Please upload at least one CSV file.")
        else:
            st.warning("Please upload both sellers.xlsx and category_tree.xlsx files.")

if __name__ == "__main__":
    main()
