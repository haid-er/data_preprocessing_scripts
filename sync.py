import os
import pandas as pd

# ------------------------------------------------------------
# Function: Compute synchronization bounds for a given folder
# ------------------------------------------------------------
def get_synchronization_bounds_for_folder(folder_path):
    """
    For all CSV files in folder_path (with no header, comma-delimited, first column is timestamp),
    compute the overlapping time window as:
       late_start = maximum of all file start timestamps, and
       early_finish = minimum of all file end timestamps.
    Returns a tuple (late_start, early_finish) or (None, None) if no valid files
    or if no overlapping interval exists.
    """
    late_start = None
    early_finish = None
    valid_file_found = False
    
    for file in os.listdir(folder_path):
        if file.lower().endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            try:
                # Read CSV file (no header, comma as delimiter)
                df = pd.read_csv(file_path, header=None, delimiter=',')
                if df.empty:
                    continue
                # Convert the first column to numeric
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
    For every CSV file in folder_path, slice rows whose first-column timestamp is
    between late_start and early_finish (bounds), and save the new file in the output_directory
    while preserving the relative folder structure.
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
                # Convert first column to numeric
                df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
                # Slice rows based on the common time window
                sliced_df = df[(df.iloc[:, 0] >= late_start) & (df.iloc[:, 0] <= early_finish)]
                new_file_path = os.path.join(new_folder, file)
                # Save without header to preserve original file format
                sliced_df.to_csv(new_file_path, index=False, header=False, sep=',')
                print(f"Synchronized file saved: {new_file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# ------------------------------------------------------------
# Function: Process entire dataset (subject/activity hierarchy)
# ------------------------------------------------------------
def process_dataset(base_directory, output_directory):
    """
    Traverse the dataset hierarchy (subjects and their activity folders).
    For each activity folder, compute the synchronization bounds and slice each CSV file accordingly.
    Synchronized files are saved to output_directory while preserving the original folder structure.
    """
    for subject in os.listdir(base_directory):
        subject_path = os.path.join(base_directory, subject)
        if os.path.isdir(subject_path):
            print(f"\nProcessing subject: {subject}")
            for activity in os.listdir(subject_path):
                activity_path = os.path.join(subject_path, activity)
                if os.path.isdir(activity_path):
                    print(f"  Activity: {activity}")
                    bounds = get_synchronization_bounds_for_folder(activity_path)
                    if bounds[0] is not None and bounds[1] is not None:
                        print(f"    Synchronization bounds: {bounds}")
                        slice_and_save_files_for_folder(activity_path, bounds, base_directory, output_directory)
                    else:
                        print(f"    Skipping activity '{activity}' due to invalid or missing bounds.")

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
    process_dataset(base_directory, output_directory)

if __name__ == "__main__":
    main()
