import os
import shutil
import pandas as pd

# ------------------------------------------------------------
# Define the selected activities list
# ------------------------------------------------------------
selected_activities = ["sitting", "walking", "jogging", "slow_walk", "clean_the_table", "downstairs", "fast_walk", "slow_walk", "laying", "reading", "standing", "talk_using_phone", "typing", "upstair"]  # Modify as needed

# ------------------------------------------------------------
# Function: Compute synchronization bounds for a given folder
# ------------------------------------------------------------
def get_synchronization_bounds_for_folder(folder_path):
    """
    Compute the overlapping time window for CSV files in a folder.
    """
    late_start = None
    early_finish = None
    valid_file_found = False
    
    for file in os.listdir(folder_path):
        if file.lower().endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path, header=None, delimiter=',')
                if df.empty:
                    continue
                df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
                if df.iloc[:, 0].isnull().all():
                    continue
                file_start = df.iloc[:, 0].min()
                file_end = df.iloc[:, 0].max()
                if pd.isnull(file_start) or pd.isnull(file_end):
                    continue
                valid_file_found = True
                if late_start is None:
                    late_start, early_finish = file_start, file_end
                else:
                    late_start = max(late_start, file_start)
                    early_finish = min(early_finish, file_end)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
    
    if not valid_file_found:
        return None, None
    if late_start > early_finish:
        print(f"No overlapping interval in folder: {folder_path}")
        return None, None
    return late_start, early_finish

# ------------------------------------------------------------
# Function: Slice and save CSV files based on computed bounds
# ------------------------------------------------------------
def slice_and_save_files_for_folder(folder_path, bounds, base_directory, output_directory):
    """
    Slice CSV files within the computed synchronization bounds and save them.
    """
    if bounds[0] is None or bounds[1] is None:
        print(f"Skipping folder {folder_path} due to invalid bounds.")
        return
    
    late_start, early_finish = bounds
    relative_folder = os.path.relpath(folder_path, base_directory)
    new_folder = os.path.join(output_directory, relative_folder)
    os.makedirs(new_folder, exist_ok=True)
    
    for file in os.listdir(folder_path):
        if file.lower().endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path, header=None, delimiter=',')
                if df.empty:
                    continue
                df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
                sliced_df = df[(df.iloc[:, 0] >= late_start) & (df.iloc[:, 0] <= early_finish)]
                new_file_path = os.path.join(new_folder, file)
                sliced_df.to_csv(new_file_path, index=False, header=False, sep=',')
                print(f"Synchronized file saved: {new_file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# ------------------------------------------------------------
# Function: Copy unselected activity folders
# ------------------------------------------------------------
def copy_folder_contents(src_folder, dest_folder):
    """
    Copy all files from the source folder to the destination folder.
    """
    os.makedirs(dest_folder, exist_ok=True)
    for file in os.listdir(src_folder):
        src_file = os.path.join(src_folder, file)
        dest_file = os.path.join(dest_folder, file)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dest_file)
            print(f"Copied: {src_file} -> {dest_file}")

# ------------------------------------------------------------
# Function: Process selected and unselected activities
# ------------------------------------------------------------
def process_activities(base_directory, output_directory):
    """
    Process only the selected activities for synchronization, 
    and copy unselected activities without modification.
    """
    for subject in os.listdir(base_directory):
        subject_path = os.path.join(base_directory, subject)
        if not os.path.isdir(subject_path):
            continue  # Skip if not a directory
        
        print(f"\nProcessing subject: {subject}")
        subject_output_path = os.path.join(output_directory, subject)
        os.makedirs(subject_output_path, exist_ok=True)

        for activity in os.listdir(subject_path):
            activity_path = os.path.join(subject_path, activity)
            if not os.path.isdir(activity_path):
                continue  # Skip non-folder items
            
            new_activity_path = os.path.join(subject_output_path, activity)
            if activity in selected_activities:
                print(f"  Synchronizing activity: {activity}")
                bounds = get_synchronization_bounds_for_folder(activity_path)
                if bounds[0] is not None and bounds[1] is not None:
                    print(f"    Synchronization bounds: {bounds}")
                    slice_and_save_files_for_folder(activity_path, bounds, base_directory, output_directory)
                else:
                    print(f"    Skipping activity '{activity}' due to invalid or missing bounds.")
            else:
                print(f"  Copying unselected activity: {activity}")
                copy_folder_contents(activity_path, new_activity_path)

# ------------------------------------------------------------
# Main function
# ------------------------------------------------------------
def main():
    base_directory = input("Enter the base dataset folder path (e.g. F:\\ServerData\\StructuredDataSet): ").strip()
    if not os.path.exists(base_directory):
        print("Base directory does not exist. Exiting.")
        return
    output_directory = input("Enter the output folder path for synchronized data: ").strip()
    if not output_directory:
        print("No output folder provided. Exiting.")
        return
    os.makedirs(output_directory, exist_ok=True)
    process_activities(base_directory, output_directory)

if __name__ == "__main__":
    main()
