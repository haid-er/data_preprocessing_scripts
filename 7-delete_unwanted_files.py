import os

KEYWORDS = ['interrupt', 'calibrated', 'uncalibrated', 'gravity', 'linear_acceleration']

def delete_matching_files(base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if any(keyword in file.lower() for keyword in KEYWORDS):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    base_path = input("Enter the base path for Structured_Data folders: ").strip()
    if os.path.exists(base_path):
        delete_matching_files(base_path)
        print("\nDeletion complete.")
    else:
        print("The specified path does not exist.")
