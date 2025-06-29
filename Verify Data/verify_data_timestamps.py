import os

def process_file(filepath):
    """
    Process a CSV file:
      - Reads non-empty lines.
      - Extracts the timestamp (assumed to be the first value on each line).
      - Returns the first timestamp, the last timestamp, and the total number of lines.
    """
    try:
        with open(filepath, 'r') as f:
            # Read all nonempty lines (strip whitespace)
            lines = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None, None, 0

    if not lines:
        return None, None, 0

    try:
        # Assume CSV format: timestamp, sensorData
        first_ts_str = lines[0].split(',')[0].strip()
        last_ts_str  = lines[-1].split(',')[0].strip()
        first_ts = int(first_ts_str)
        last_ts = int(last_ts_str)
    except Exception as e:
        print(f"Error processing timestamps in file {filepath}: {e}")
        first_ts = None
        last_ts = None

    return first_ts, last_ts, len(lines)

def main():
    # Prompt for the root folder (where the data is stored)
    root = input("Enter the root folder path (default: F:\\ServerData\\jan21): ").strip()
    if not root:
        root = r"F:\ServerData\jan21"

    # Prompt for user name and activity
    user = input("Enter the user name: ").strip()
    activity = input("Enter the activity: ").strip()

    print(f"\nVerifying data for user '{user}' and activity '{activity}' in the folder structure under '{root}'\n")
    
    # Print header of the table
    header = f"{'File Name':<40} {'Start Time':>20} {'End Time':>20}"
    print(header)
    print("-" * len(header))
    
    # List all subdirectories in root. Each one should be a source (like mobile, watch, glasses, etc.)
    try:
        sources = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
    except Exception as e:
        print(f"Error reading root folder '{root}': {e}")
        return

    if not sources:
        print("No source folders found in the root directory.")
        return

    # Process each source folder.
    for source in sources:
        # Build the expected folder path: root\source\user\activity
        target_folder = os.path.join(root, source, user, activity)
        print(f"\nChecking folder for source '{source}':")
        if os.path.isdir(target_folder):
            # List all CSV files in this folder
            csv_files = [f for f in os.listdir(target_folder) if f.lower().endswith('.csv')]
            if not csv_files:
                print("  No CSV files found in this folder.")
            else:
                for file in sorted(csv_files):
                    filepath = os.path.join(target_folder, file)
                    first_ts, last_ts, count = process_file(filepath)
                    if first_ts is None or last_ts is None:
                        print(f"{file:<55} {'N/A':>20} {'N/A':>20}")
                    else:
                        print(f"{file:<55} {first_ts:>20} {last_ts:>20}")
        else:
            print(f"  Expected folder does not exist: {target_folder}")

if __name__ == "__main__":
    main()
