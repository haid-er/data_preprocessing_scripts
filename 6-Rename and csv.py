import os
import csv

def rename_subfolders_and_generate_csv():
    parent_folder = input("Enter the path to the parent folder: ").strip()
    parent_folder = os.path.abspath(os.path.expanduser(parent_folder))
    
    if not os.path.isdir(parent_folder):
        print("The parent folder path does not exist or is not a directory.")
        return
    
    try:
        subfolders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]
    except Exception as e:
        print(f"Error accessing the parent folder: {e}")
        return
    
    if not subfolders:
        print("No subfolders found in the given folder.")
        return
    
    csv_path = input("Enter the full path (including filename) where the CSV should be saved/appended: ").strip()
    csv_path = os.path.abspath(os.path.expanduser(csv_path))
    
    old_new_names = []
    
    for idx, old_name in enumerate(subfolders, start=1):
        old_path = os.path.join(parent_folder, old_name)
        new_name = f"sub{idx}"
        new_path = os.path.join(parent_folder, new_name)
        
        # Avoid overwriting existing folders
        count = 1
        temp_new_path = new_path
        while os.path.exists(temp_new_path):
            temp_new_path = os.path.join(parent_folder, f"{new_name}_{count}")
            count += 1
        new_path = temp_new_path
        
        try:
            os.rename(old_path, new_path)
            new_folder_name = os.path.basename(new_path)
            old_new_names.append((old_name, new_folder_name))
        except Exception as e:
            print(f"Failed to rename folder '{old_name}': {e}")
    
    # Append mode 'a' to add rows without overwriting existing CSV content
    try:
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        file_exists = os.path.isfile(csv_path)
        with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header only if file did not exist before
            if not file_exists:
                writer.writerow(['old folder name', 'new folder name'])
            writer.writerows(old_new_names)
        print(f"\nRenaming complete. CSV file saved/appended at: {csv_path}")
    except Exception as e:
        print(f"Failed to write/append CSV file: {e}")

if __name__ == "__main__":
    rename_subfolders_and_generate_csv()
