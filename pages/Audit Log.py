
import pandas as pd
import numpy as np
import os
import streamlit as st

def process_audit_log(script_folder, main_file_path, sellers_file_path):
    try:
        # Read the main file and sellers file into DataFrames
        if main_file_path.lower().endswith('.csv'):
            # Specify the data types to avoid DtypeWarning
            dtype_options = {'Created At': 'str', 'Event': 'str', 'User': 'str', 'Description': 'str', 'IP Address': 'str'}
            main_df = pd.read_csv(main_file_path, delimiter=';', dtype=dtype_options)
        else:
            main_df = pd.read_excel(main_file_path, engine='openpyxl')

        # Remove ") has been created" from the 'Description' column
        main_df['Description'] = main_df['Description'].str.replace(') has been created', '')

        # Extract the last word and create a new column 'SKU'
        main_df['SKU'] = main_df['Description'].str.split().str[-1]

        # Read the sellers file
        sellers_df = pd.read_excel(sellers_file_path, engine='openpyxl')

        # Perform VLOOKUP to add a 'Seller_ID' column to the main file
        merged_df = pd.merge(main_df, sellers_df[['User', 'Seller_ID']], on='User', how='left')

        # Keep only 'Seller_ID' and 'SKU' columns
        result_df = merged_df[['Seller_ID', 'SKU']].copy()

        # Rename columns
        result_df.rename(columns={'Seller_ID': 'SellerID', 'SKU': 'SellerSku'}, inplace=True)

        # Add new columns and set 'Approved' to 'Yes' using .loc
        result_df.loc[:, 'Approved'] = 'Yes'
        result_df.loc[:, 'Reject Reason Ids'] = ''
        result_df.loc[:, 'Rejection Message'] = ''

        # Save the modified DataFrame to a new CSV file based on the original format
        output_folder_name = f'output_{pd.Timestamp.now().strftime("%Y-%m-%d_%H%M%S")}'
        os.makedirs(output_folder_name, exist_ok=True)

        chunk_size = 80000
        chunks = [result_df[i:i + chunk_size] for i in range(0, len(result_df), chunk_size)]

        for i, chunk in enumerate(chunks):
            output_file_path = os.path.join(output_folder_name, f'Chunk_{chr(ord("A") + i)}_{os.path.basename(main_file_path)}.csv')
            chunk.to_csv(output_file_path, index=False, sep=';')

        st.success(f'Modified data saved to the new folder: {output_folder_name}')

    except FileNotFoundError as file_not_found_error:
        st.error(f"Error: {file_not_found_error}. Please make sure the files exist.")
    except pd.errors.ParserError as parser_error:
        st.error(f"Error parsing the input files: {parser_error}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def main():
    st.title("Audit Log Processor")

    # Specify the script folder path
    script_folder = os.path.dirname(os.path.abspath(__file__))
    
    # Find all files in the script folder
    all_files = os.listdir(script_folder)

    # Filter files that start with 'AuditLogEntry' and have valid extensions
    main_files = [file for file in all_files if file.startswith('AuditLogEntry') and file.lower().endswith(('.xls', '.xlsx', '.ods', '.csv'))]

    if not main_files:
        st.error(f"No matching files found with pattern: AuditLogEntry*.{xls,xlsx,ods,csv}")
        st.stop()

    # Choose the latest modified file
    main_file_path = st.file_uploader("Upload Audit Log File", type=["xlsx", "xls", "csv"])

    if not main_file_path:
        st.warning("Please upload the audit log file.")
        st.stop()

    st.info(f"Selected main file: {os.path.basename(main_file_path.name)}")

    # Select sellers file
    sellers_file_path = st.file_uploader("Upload Sellers File", type=["xlsx", "xls", "csv"])

    if not sellers_file_path:
        st.warning("Please upload the sellers file.")
        st.stop()

    process_audit_log(script_folder, main_file_path, sellers_file_path)

if __name__ == "__main__":
    main()
