import os
import pandas as pd

def count_values_in_csv(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        # Count the non-null values in the file
        print(f"{file_path},, {df.notnull().sum()}")
        return df.notnull().sum().sum()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0

def traverse_and_count(directory):
    folder_counts = {}

    # Walk through the directory
    for root, _, files in os.walk(directory):
        folder_name = os.path.relpath(root, directory)  # Relative folder name
        if folder_name == ".":
            folder_name = "Testing"  # Rename the base folder for clarity
        
        total_count = 0
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                total_count += count_values_in_csv(file_path)
        
        folder_counts[folder_name] = total_count
    
    return folder_counts

def main():
    # Replace this with the path to your HAR_DATA folder
    base_directory = "F:\ServerData"
    counts = traverse_and_count(base_directory)
    
    # for folder, count in counts.items():
        # print(f"Folder: {folder}, Total Values: {count}")

if __name__ == "__main__":
    main()
