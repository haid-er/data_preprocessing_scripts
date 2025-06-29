import os
import pandas as pd

# ------------------------------------------------------------
# Function to process a CSV file and extract its start and end timestamps.
# Assumes files have no header, use a comma as the delimiter, and the first column is the timestamp.
# ------------------------------------------------------------
def process_file_timestamps(filepath):
    """
    Reads a CSV file (with no header and comma as delimiter) and returns:
      - start_ts: the first timestamp in the file (converted to numeric)
      - end_ts: the last timestamp in the file (converted to numeric)
    """
    try:
        # Read the file without header using comma as the delimiter
        df = pd.read_csv(filepath, header=None, delimiter=',')
        if df.empty:
            return None, None
        # Convert the first column to numeric values
        start_ts = pd.to_numeric(df.iloc[0, 0], errors='coerce')
        end_ts = pd.to_numeric(df.iloc[-1, 0], errors='coerce')
        if pd.isna(start_ts) or pd.isna(end_ts):
            raise ValueError("Timestamps could not be converted to numbers.")
        return start_ts, end_ts
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")
        return None, None

# ------------------------------------------------------------
# Main function: Recursively traverse the folder structure and print start and end timestamps for each CSV file.
# ------------------------------------------------------------
def main():
    root = input("Enter the root folder path for synchronized data: ").strip()
    if not os.path.exists(root):
        print("Directory does not exist. Exiting.")
        return

    # Print header for the output table
    header = f"{'File Path':<60} {'Start Time':>20} {'End Time':>20}"
    print(header)
    print("-" * len(header))

    # Walk through the directory structure
    for dirpath, _, filenames in os.walk(root):
        for file in filenames:
            if file.lower().endswith('.csv'):
                filepath = os.path.join(dirpath, file)
                start_ts, end_ts = process_file_timestamps(filepath)
                if start_ts is not None and end_ts is not None:
                    print(f"{filepath:<120} {start_ts:>20} {end_ts:>20}")

if __name__ == "__main__":
    main()
