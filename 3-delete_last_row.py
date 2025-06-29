import os

def remove_last_line(filepath):
    """
    Opens the file at filepath, reads all lines,
    and writes back all lines except the last one.
    """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        if not lines:
            return  # nothing to do on an empty file

        # Remove the last line
        new_lines = lines[:-1]
        
        with open(filepath, 'w') as f:
            f.writelines(new_lines)
        
        print(f"Processed: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def process_directory(root_dir):
    """
    Recursively walk through root_dir and process all .csv files.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            if file.lower().endswith('.csv'):
                full_path = os.path.join(dirpath, file)
                remove_last_line(full_path)

def main():
    root = input("Enter the root folder path (e.g. F:\\ServerData\\jan21): ").strip()
    if not root:
        print("No folder provided. Exiting.")
        return
    process_directory(root)

if __name__ == "__main__":
    main()
