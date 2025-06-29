import os
import pandas as pd

# ------------------------------------------------------------
# Function to process each CSV file in the synchronized data folder.
# Assumes that the files have no header, are comma-delimited, and
# that the first column contains the timestamp.
# ------------------------------------------------------------
def process_file(filepath):
    """
    Reads a CSV file with no header and comma as delimiter, and returns:
      - total_rows: the number of data rows in the file
      - total_time: the difference between the last and first timestamp (numeric)
    """
    try:
        # Read the CSV using comma as the delimiter (adjust if needed)
        df = pd.read_csv(filepath, header=None, delimiter=',')
        if df.empty:
            return 0, 0

        # Convert the first column (timestamps) to numeric values
        first_ts = pd.to_numeric(df.iloc[0, 0], errors='coerce')
        last_ts = pd.to_numeric(df.iloc[-1, 0], errors='coerce')
        if pd.isna(first_ts) or pd.isna(last_ts):
            raise ValueError("Timestamps could not be converted to numbers.")
        total_rows = len(df)
        total_time = last_ts - first_ts
        return total_rows, total_time
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")
        return None, None

# ------------------------------------------------------------
# Main function: recursively traverse the folder and print statistics.
# ------------------------------------------------------------
def main():
    root = input("Enter the root folder path for synchronized data: ").strip()
    if not os.path.exists(root):
        print("Directory does not exist. Exiting.")
        return

    # Print header for the table
    header = f"{'File Path':<60} {'Total Values':>15} {'Total Time':>15}"
    print(header)
    print("-" * len(header))

    # Walk through the directory structure
    for dirpath, _, filenames in os.walk(root):
        for file in filenames:
            if file.lower().endswith('.csv'):
                filepath = os.path.join(dirpath, file)
                total_rows, total_time = process_file(filepath)
                if total_rows is not None:
                    print(f"{filepath:<120} {total_rows:>15} {total_time:>15}")

if __name__ == "__main__":
    main()
