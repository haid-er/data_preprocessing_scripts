import os
import re
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def clean_filename(file_name):
    """
    Remove redundant patterns like '_eX.csv_eX.csv' from the filename.
    For example, convert 'watch_magnetometer_e15.csv_e15.csv' to 'watch_magnetometer_e15.csv'.
    """
    cleaned_name = re.sub(r'(_e\d+\.csv)_e\d+\.csv$', r'\1', file_name)
    return cleaned_name

def parse_file_info(file_path, base_path):
    """
    Extract subject, activity, sensor name, and event number from file path.
    
    Assumes the hierarchy: base_path/subject/activity/filename
    and that the filename contains an event part in the form '_eXX.csv'.
    
    Returns:
      (subject, activity, sensor, event_num)
    """
    rel_path = os.path.relpath(file_path, base_path)
    parts = rel_path.split(os.sep)
    if len(parts) < 3:
        return None, None, None, None
    subject = parts[0]
    activity = parts[1]
    filename = os.path.basename(file_path)
    match = re.search(r'^(.*)_e0*(\d+)\.csv$', filename, re.IGNORECASE)
    if match:
        sensor = match.group(1)  # e.g., 'watch_magnetometer_uncalibrated' or 'watch_accelerometer'
        event_num = int(match.group(2))
    else:
        sensor, event_num = None, None
    return subject, activity, sensor, event_num

def load_sensor_data(file_path):
    """
    Load sensor data from a CSV file.
    
    Reads the CSV file (assumed to have no header, comma-delimited).
    If the file has 4 or more columns, only the first 4 columns are used and renamed to:
         ['timestamp', 'x', 'y', 'z'].
    Otherwise, the columns are assumed to be ['x','y','z'].
    
    Returns:
      A pandas DataFrame with the sensor data.
    """
    try:
        df = pd.read_csv(file_path, delimiter=",", header=None)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
    if df.shape[1] >= 4:
        df = df.iloc[:, :4]
        df.columns = ['timestamp', 'x', 'y', 'z']
    else:
        df.columns = ['x', 'y', 'z']
    return df

def plot_comparison_graph(base_file, other_files, sensor_keyword, subject_base, event_base, activity, dest_file):
    """
    Plot the comparison graph.
    
    Loads the base_file and each file from other_files (a list of tuples (subject, event, file_path)),
    extracts the 'x' column data from each file, and plots them on a single graph.
    
    The base file is labeled as '{subject_base}_e{event_base} (base)' and each other file is labeled as
    '{subject}_e{event}'. The graph title includes the sensor keyword and activity.
    
    The final graph is saved as a PNG file at dest_file.
    """
    plt.figure(figsize=(12, 7))
    
    # Load and plot base file data (using the x column)
    df_base = load_sensor_data(base_file)
    if df_base is None:
        print(f"Could not load base file: {base_file}")
        return
    plt.plot(df_base['x'].values, label=f"{subject_base}_e{event_base} (base)")
    
    # Plot data for each other subject event file
    for subj, ev, fpath in other_files:
        df = load_sensor_data(fpath)
        if df is not None:
            plt.plot(df['x'].values, label=f"{subj}_e{ev}")
    
    plt.title(f"Comparison for Sensor: {sensor_keyword}\nActivity: {activity}")
    plt.xlabel("Time (samples)")
    plt.ylabel("X Value")
    plt.legend(loc="best")
    plt.grid(True)
    
    plt.savefig(dest_file)
    plt.close()
    print(f"Saved comparison graph: {dest_file}")

def find_event_file(base_path, subject, activity, sensor_keyword, event_number):
    """
    Search for a CSV file under base_path/subject/activity that contains the sensor_keyword and
    the specified event number (in the form '_eXX.csv').
    
    Returns the full file path if found; otherwise, returns None.
    """
    search_pattern = os.path.join(base_path, subject, activity, "*.csv")
    files = glob.glob(search_pattern)
    for f in files:
        fbase = os.path.basename(f)
        fclean = clean_filename(fbase)
        if sensor_keyword.lower() in fclean.lower():
            match = re.search(r'_e0*(\d+)\.csv$', fclean, re.IGNORECASE)
            if match and int(match.group(1)) == event_number:
                return f
    return None

def main():
    # Prompt for the source structured data folder
    base_path = input("Enter the path to the structured data folder: ").strip()
    while not os.path.exists(base_path):
        print("Path does not exist.")
        base_path = input("Enter the path to the structured data folder: ").strip()
    
    # Prompt for base subject, activity, sensor keyword, and base event number
    subject_base = input("Enter the BASE subject ID (e.g., BITF21M541): ").strip()
    activity = input("Enter the activity (e.g., walking): ").strip()
    sensor_keyword = input("Enter the sensor keyword (e.g., watch_gyroscope): ").strip()
    try:
        event_base = int(input(f"Enter the BASE event number for subject {subject_base}: ").strip())
    except Exception as e:
        print("Invalid event number. Exiting.")
        return
    
    # Find the base event file for the base subject
    base_file = find_event_file(base_path, subject_base, activity, sensor_keyword, event_base)
    if base_file is None:
        print(f"Base file not found for {subject_base} in activity {activity} with sensor {sensor_keyword} and event {event_base}.")
        return
    
    # Prompt for other subjects to compare (comma-separated list)
    other_subjects_input = input("Enter other subject IDs to compare (comma-separated): ").strip()
    other_subjects = [s.strip() for s in other_subjects_input.split(",") if s.strip()]
    
    # For each other subject, prompt for the event number to use and find the corresponding file
    other_subjects_events = []  # list of tuples: (subject, event, file_path)
    for subj in other_subjects:
        try:
            ev = int(input(f"Enter event number for subject {subj}: ").strip())
        except Exception as e:
            print(f"Invalid event number for subject {subj}. Skipping.")
            continue
        file_path = find_event_file(base_path, subj, activity, sensor_keyword, ev)
        if file_path:
            other_subjects_events.append((subj, ev, file_path))
        else:
            print(f"File not found for subject {subj} with event {ev}.")
    
    if not other_subjects_events:
        print("No comparison files found. Exiting.")
        return
    
    # Prompt for destination folder to save the comparison graph
    dest_dir = input("Enter the destination folder for the comparison graph: ").strip()
    os.makedirs(dest_dir, exist_ok=True)
    
    # Create a destination file name using base subject, sensor, base event, and activity
    dest_file = os.path.join(dest_dir, f"{subject_base}_{sensor_keyword}_e{event_base}_{activity}_comparison.png")
    
    # Plot the comparison graph using the base file and other subject event files
    plot_comparison_graph(base_file, other_subjects_events, sensor_keyword, subject_base, event_base, activity, dest_file)

if __name__ == "__main__":
    main()
