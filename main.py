import pandas as pd
import os


def process_sales_data(input_files, output_file):
    """
    Processes multiple sales CSV files to filter for 'pink morsel',
    calculate sales, select relevant columns, and save to a new CSV.

    Args:
        input_files (list): A list of paths to the input CSV files.
        output_file (str): The path to save the formatted output CSV file.
    """
    all_data_frames = []

    for file_path in input_files:
        if not os.path.exists(file_path):
            print(f"Warning: File not found at {file_path}. Skipping.")
            continue

        try:
            # Read the CSV file
            df = pd.read_csv(file_path)

            # 1. Filter for "pink morsel"
            df_pink = df[
                df['product'].str.lower() == 'pink morsel'].copy()  # Use .copy() to avoid SettingWithCopyWarning

            if df_pink.empty:
                print(f"No 'pink morsel' data found in {file_path}. Skipping.")
                continue

            # 2. Process 'price' and 'quantity' to calculate 'sales'
            # Remove '$' from price and convert to float
            df_pink.loc[:, 'price'] = df_pink['price'].replace({'\$': ''}, regex=True).astype(float)
            # Ensure quantity is numeric
            df_pink.loc[:, 'quantity'] = pd.to_numeric(df_pink['quantity'])

            df_pink.loc[:, 'Sales'] = df_pink['price'] * df_pink['quantity']

            # 3. Select and rename columns for the output
            # The date field is useful as is ('date')
            # The region field is useful as is ('region')
            df_output = df_pink[['Sales', 'date', 'region']].copy()  # Use .copy()
            df_output.rename(columns={'date': 'Date', 'region': 'Region'}, inplace=True)

            all_data_frames.append(df_output)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    if not all_data_frames:
        print("No data processed. Output file will not be created.")
        return

    # Combine all processed data
    combined_df = pd.concat(all_data_frames, ignore_index=True)

    # Save to the output file
    try:
        combined_df.to_csv(output_file, index=False)
        print(f"Successfully processed data and saved to {output_file}")
        print("\nFirst 5 rows of the output:")
        print(combined_df.head())
    except Exception as e:
        print(f"Error saving output file {output_file}: {e}")


# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# INSTRUCTIONS FOR USE:
# 1. Make sure you have pandas installed:
#    pip install pandas
#
# 2. Save this script as a Python file (e.g., process_data.py) in the
#    same directory where your 'data' folder (containing the CSVs) is.
#    Or, adjust the file paths accordingly.
#
# 3. Create a 'data' folder in the same directory as your script,
#    and place your CSV files (daily_sales_data_0.csv,
#    daily_sales_data_1.csv, daily_sales_data_2.csv) inside it.
#    If your files are in a different location, modify the `input_file_paths`.
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

if __name__ == "__main__":
    # Assuming the CSV files are in a subdirectory named 'data'
    # relative to where the script is run.
    data_folder = 'data'
    input_file_names = [
        'daily_sales_data_0.csv',
        'daily_sales_data_1.csv',
        'daily_sales_data_2.csv'
    ]

    # Construct full paths to input files
    input_file_paths = [os.path.join(data_folder, fname) for fname in input_file_names]

    output_file_path = 'formatted_pink_morsel_sales.csv'  # Output file will be in the same directory as the script

    process_sales_data(input_file_paths, output_file_path)