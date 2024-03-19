import pandas as pd
import numpy as np
import os
import streamlit as st
import zipfile

def main():
    st.title("Audit Log Processor")

    # File uploader for the main audit log file
    main_file = st.file_uploader("Upload Audit Log File", type=["xlsx", "xls", "csv"])

    if main_file is None:
        st.warning("Please upload the audit log file.")
        st.stop()

    # File uploader for the sellers file
    sellers_file = st.file_uploader("Upload Sellers File", type=["xlsx", "xls", "csv"])

    if sellers_file is None:
        st.warning("Please upload the sellers file.")
        st.stop()

    try:
        # Read the main file and sellers file into DataFrames
        main_df = pd.read_excel(main_file, engine='openpyxl') if main_file.name.lower().endswith(('.xls', '.xlsx')) else pd.read_csv(main_file, delimiter=';')
        
        # Display number of rows in the input file
        st.write(f"Number of rows in input file: {len(main_df)}")

        # Remove ") has been created" from the 'Description' column
        main_df['Description'] = main_df['Description'].str.replace(') has been created', '')

        # Extract the last word and create a new column 'SKU'
        main_df['SKU'] = main_df['Description'].str.split().str[-1]

        # Read the sellers file
        sellers_df = pd.read_excel(sellers_file, engine='openpyxl')

        # Perform VLOOKUP to add a 'Seller_ID' column to the main file
        merged_df = pd.merge(main_df, sellers_df[['User', 'Seller_ID']], on='User', how='left')

        # Keep only 'Seller_ID' and 'SKU' columns
        result_df = merged_df[['Seller_ID', 'SKU']].copy()

        # Rename columns
        result_df.rename(columns={'Seller_ID': 'SellerID', 'SKU': 'SellerSku'}, inplace=True)

        # Add new columns and set 'Approved' to 'Yes'
        result_df['Approved'] = 'Yes'
        result_df['Reject Reason Ids'] = ''
        result_df['Rejection Message'] = ''

        # Get user input for number of rows in each chunk
        chunk_size = st.number_input("Enter the number of rows in each chunk of the output files", min_value=1, value=1000)

        # Save the modified DataFrame to a new folder
        output_folder_name = f'output_{pd.Timestamp.now().strftime("%Y-%m-%d_%H%M%S")}'
        os.makedirs(output_folder_name, exist_ok=True)

        chunks = [result_df[i:i + chunk_size] for i in range(0, len(result_df), chunk_size)]

        for i, chunk in enumerate(chunks):
            output_file_path = os.path.join(output_folder_name, f'Chunk_{chr(ord("A") + i)}_{main_file.name}.csv')
            chunk.to_csv(output_file_path, index=False, sep=';')

        st.success(f'Modified data saved to the new folder: {output_folder_name}')

        # Create download buttons for each output file
        for i, chunk in enumerate(chunks):
            st.download_button(label=f"Download Chunk {chr(ord('A') + i)}", data=chunk.to_csv(index=False, sep=';'), file_name=f"Chunk_{chr(ord('A') + i)}_{main_file.name}.csv", mime="text/csv")

        # Create a button to download a zip file of all output files
        with st.spinner("Creating zip file..."):
            with zipfile.ZipFile(f"{output_folder_name}.zip", "w") as zipf:
                for filename in os.listdir(output_folder_name):
                    filepath = os.path.join(output_folder_name, filename)
                    zipf.write(filepath, arcname=filename)

        st.success("Zip file created successfully.")
        st.download_button(label="Download All as Zip", data=open(f"{output_folder_name}.zip", "rb").read(), file_name=f"{output_folder_name}.zip", mime="application/zip")

    except FileNotFoundError as file_not_found_error:
        st.error(f"Error: {file_not_found_error}. Please make sure the files exist.")
    except pd.errors.ParserError as parser_error:
        st.error(f"Error parsing the input files: {parser_error}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
