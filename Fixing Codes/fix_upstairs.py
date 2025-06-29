import os
import pandas as pd
import re

# Only process these two activities
selected_activities = {"upstairs", "downstairs"}

# Duration threshold in milliseconds
MIN_DURATION_MS = 10000  # 10 seconds
EVENT_DURATION_MS = 5000  # 5 seconds


def clean_wrong_naming(activity_folder):
    """
    Scan CSV files in activity_folder for filenames with multiple '_e<index>' segments
    and rename them to have only one suffix with the last index. E.g.,
    'glass_accelerometer_e0_e1.csv' -> 'glass_accelerometer_e1.csv'.
    """
    for fname in os.listdir(activity_folder):
        if not fname.lower().endswith('.csv'):
            continue
        # Match patterns with multiple _e<number> segments before .csv
        # Regex: capture base prefix and all trailing _e<num> groups
        m = re.match(r'^(.*?)(_e\d+)+\.csv$', fname)
        if m:
            # Extract all indices
            # Find all suffixes
            indices = re.findall(r'_e(\d+)', fname)
            if len(indices) > 1:
                # Use last index
                last_idx = indices[-1]
                # Derive prefix before first _e
                prefix = re.sub(r'(_e\d+)+\.csv$', '', fname)
                # But prefix may still contain _e<num> if nested; better strip all
                prefix = re.sub(r'(_e\d+)+$', '', prefix)
                new_name = f"{prefix}_e{last_idx}.csv"
                old_path = os.path.join(activity_folder, fname)
                new_path = os.path.join(activity_folder, new_name)
                # Avoid overwriting existing correct file
                if os.path.exists(new_path):
                    print(f"Conflict: {new_name} already exists; cannot rename {fname}.")
                else:
                    try:
                        os.rename(old_path, new_path)
                        print(f"Renamed wrong file '{fname}' to '{new_name}'")
                    except Exception as e:
                        print(f"Error renaming '{fname}': {e}")


def split_file_into_events_single(file_path):
    """
    Split a CSV file at file_path into consecutive 5-second events starting from e0.
    Original file is deleted after splitting. Returns count of events created.
    """
    try:
        df = pd.read_csv(file_path, header=None, delimiter=',')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0

    if df.empty:
        print(f"File {file_path} is empty. Skipping.")
        return 0

    # Convert first column to numeric timestamps
    try:
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    except Exception as e:
        print(f"Error converting timestamps in {file_path}: {e}")
        return 0

    if df.iloc[:, 0].isnull().all():
        print(f"File {file_path} has invalid timestamps. Skipping.")
        return 0

    start_ts = df.iloc[0, 0]
    end_ts = df.iloc[-1, 0]
    total_duration = end_ts - start_ts

    if total_duration < MIN_DURATION_MS:
        # Skip files shorter than 10 seconds
        return 0

    num_events = int(total_duration // EVENT_DURATION_MS)
    folder, original_file = os.path.split(file_path)
    base_name, ext = os.path.splitext(original_file)
    # Derive prefix by stripping any existing _e<number> suffix
    prefix = re.sub(r'_e\d+$', '', base_name)

    events_created = 0
    for i in range(num_events):
        event_start = start_ts + i * EVENT_DURATION_MS
        event_end = start_ts + (i + 1) * EVENT_DURATION_MS
        event_df = df[(df.iloc[:, 0] >= event_start) & (df.iloc[:, 0] < event_end)]
        if event_df.empty:
            continue
        new_file_name = f"{prefix}_e{i}{ext}"
        new_file_path = os.path.join(folder, new_file_name)
        # If file exists (from previous run), skip to prevent overwrite
        if os.path.exists(new_file_path):
            print(f"File {new_file_name} already exists. Skipping to prevent overwrite.")
            events_created += 1
            continue
        try:
            event_df.to_csv(new_file_path, index=False, header=False)
            events_created += 1
        except Exception as e:
            print(f"Error saving {new_file_path}: {e}")

    if events_created > 0:
        try:
            os.remove(file_path)
            print(f"Deleted original file: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    return events_created


def process_activity_folder(activity_folder):
    print(f"\nProcessing activity folder: {activity_folder}")
    # First, clean wrong-named files
    clean_wrong_naming(activity_folder)
    # Then split each file independently
    for fname in sorted(os.listdir(activity_folder)):
        if fname.lower().endswith('.csv'):
            file_path = os.path.join(activity_folder, fname)
            if os.path.isfile(file_path):
                split_file_into_events_single(file_path)


def process_subject_folder(subject_folder):
    for activity in os.listdir(subject_folder):
        if activity.lower() in selected_activities:
            activity_folder = os.path.join(subject_folder, activity)
            if os.path.isdir(activity_folder):
                process_activity_folder(activity_folder)


def process_dataset(base_directory):
    for subject in os.listdir(base_directory):
        subject_folder = os.path.join(base_directory, subject)
        if os.path.isdir(subject_folder):
            print(f"Processing subject: {subject}")
            process_subject_folder(subject_folder)


def main():
    base_directory = input("Enter the base dataset folder path: ").strip()
    if not os.path.exists(base_directory):
        print("Directory does not exist.")
        return
    process_dataset(base_directory)

if __name__ == "__main__":
    main()
