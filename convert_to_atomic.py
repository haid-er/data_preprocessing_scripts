import os
import pandas as pd

# -------------------------------------------------------------------
# Dictionary of activities to process (keys should be lowercase)
# Only folders whose name (lowercase) is in this dictionary will be processed.
# -------------------------------------------------------------------
selected_activities = {
    "fast_walk": True,
    # "quick_walk": True,
    # "jogging": True,
    # "laying": True,
    # "reading": True,
    # "sitting": True,
    # "slow_walk": True,
    # "standing": True,
    # "talk_using_phone": True,
    # "typing": True,
    # "walking": True,
    # "clean_the_table": True,
    # "downstairs": True,
    # "upstairs": True,
}

# -------------------------------------------------------------------
# Function to split a single CSV file (synchronized) into consecutive 5-second events.
# Assumptions:
#   - The file has no header.
#   - The delimiter is a comma.
#   - The first column contains the timestamp (in milliseconds).
# Only files with duration >= 10 seconds (i.e. at least 2 events) are processed.
# Any extra data that does not form a full 5-second block is discarded.
# The event files are saved in the same folder as the original file.
# After successful splitting, the original (large) file is deleted.
# -------------------------------------------------------------------
def split_file_into_events(file_path, event_duration_ms=5000):
    try:
        # Read the CSV file (no header, comma-delimited)
        df = pd.read_csv(file_path, header=None, delimiter=',')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    if df.empty:
        print(f"File {file_path} is empty. Skipping.")
        return

    # Convert first column (timestamps) to numeric values
    try:
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    except Exception as e:
        print(f"Error converting timestamps in {file_path}: {e}")
        return

    if df.iloc[:, 0].isnull().all():
        print(f"File {file_path} has invalid timestamps. Skipping.")
        return

    start_ts = df.iloc[0, 0]
    end_ts = df.iloc[-1, 0]
    total_duration = end_ts - start_ts

    if total_duration < 10000:
        print(f"File {file_path} duration ({total_duration} ms) is less than 10 seconds. Skipping splitting.")
        return

    # Calculate the number of full events (each event_duration_ms long)
    num_events = int(total_duration // event_duration_ms)
    folder, original_file = os.path.split(file_path)
    base_name, ext = os.path.splitext(original_file)

    events_created = 0

    for i in range(num_events):
        event_start = start_ts + i * event_duration_ms
        event_end = start_ts + (i + 1) * event_duration_ms

        # Select rows with timestamp in [event_start, event_end)
        event_df = df[(df.iloc[:, 0] >= event_start) & (df.iloc[:, 0] < event_end)]
        if event_df.empty:
            continue

        new_file_name = f"{base_name}_e{i}{ext}"
        new_file_path = os.path.join(folder, new_file_name)
        try:
            event_df.to_csv(new_file_path, index=False, header=False, sep=',')
            print(f"Saved {new_file_path} (Event {i}, Duration: {event_duration_ms} ms, Rows: {len(event_df)})")
            events_created += 1
        except Exception as e:
            print(f"Error saving file {new_file_path}: {e}")

    # If at least one event file was created, delete the original file
    if events_created > 0:
        try:
            os.remove(file_path)
            print(f"Deleted original file: {file_path}")
        except Exception as e:
            print(f"Error deleting original file {file_path}: {e}")

# -------------------------------------------------------------------
# Process all CSV files in an activity folder.
# -------------------------------------------------------------------
def process_activity_folder(activity_folder):
    for file in os.listdir(activity_folder):
        if file.lower().endswith('.csv'):
            file_path = os.path.join(activity_folder, file)
            split_file_into_events(file_path)

# -------------------------------------------------------------------
# Process each subject folder (each subject contains several activity folders).
# Only process activity folders that are in selected_activities.
# -------------------------------------------------------------------
def process_subject_folder(subject_folder):
    for activity in os.listdir(subject_folder):
        if activity.lower() in selected_activities:
            activity_folder = os.path.join(subject_folder, activity)
            if os.path.isdir(activity_folder):
                print(f"\nProcessing activity folder: {activity_folder}")
                process_activity_folder(activity_folder)

# -------------------------------------------------------------------
# Process the entire dataset (multiple subjects).
# -------------------------------------------------------------------
def process_dataset(base_directory):
    for subject in os.listdir(base_directory):
        subject_folder = os.path.join(base_directory, subject)
        if os.path.isdir(subject_folder):
            print(f"\nProcessing subject folder: {subject_folder}")
            process_subject_folder(subject_folder)

# -------------------------------------------------------------------
# Main function: prompt for base dataset folder and process it.
# -------------------------------------------------------------------
def main():
    base_directory = input("Enter the base dataset folder path (e.g. F:\\ServerData\\SynchronizedData): ").strip()
    if not os.path.exists(base_directory):
        print("Directory does not exist.")
        return
    process_dataset(base_directory)

if __name__ == "__main__":
    main()
