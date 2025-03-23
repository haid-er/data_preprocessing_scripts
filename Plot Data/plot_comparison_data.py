import os
import re
import glob
import pandas as pd
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
        sensor = match.group(1)  # e.g., 'watch_magnetometer' or 'watch_accelerometer'
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

def plot_comparison_graph(base_file, comp_files, sensor_keyword, subject_base, base_event, activity, dest_file):
    """
    Plot the comparison graph.
    
    Loads the base_file and each file from comp_files (a list of tuples (subject, event, file_path)),
    extracts the 'x' column data from each file, and plots them on a single graph.
    
    The base file is labeled as '{subject_base}_e{base_event} (base)' and each other file is labeled as
    '{subject}_e{event}'. The graph title includes the sensor keyword and activity.
    
    The final graph is saved as a PNG file at dest_file.
    """
    plt.figure(figsize=(12, 7))
    
    # Load and plot base file data (using the x column)
    df_base = load_sensor_data(base_file)
    if df_base is None:
        print(f"Could not load base file: {base_file}")
        return
    plt.plot(df_base['x'].values, label=f"{subject_base}_e{base_event} (base)")
    
    # Plot data for each compared subject event file
    for subj, ev, fpath in comp_files:
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
        # Extract sensor using parse_file_info
        _, _, sensor, _ = parse_file_info(f, base_path)
        # Compare sensor exactly
        if sensor and sensor.lower() == sensor_keyword.lower():
            match = re.search(r'_e0*(\d+)\.csv$', fclean, re.IGNORECASE)
            if match and int(match.group(1)) == event_number:
                return f
    return None

def main():
    # Get the source dataset folder and destination folder for plots.
    base_path = input("Enter the path to the structured dataset folder: ").strip()
    while not os.path.exists(base_path):
        print("Path does not exist.")
        base_path = input("Enter the path to the structured dataset folder: ").strip()
        
    dest_base = input("Enter the destination folder for plotted graphs: ").strip()
    os.makedirs(dest_base, exist_ok=True)
    
    # Get base subject and its base event number.
    subject_base = input("Enter the BASE subject ID (e.g., BITF21M541): ").strip()
    try:
        base_event = int(input(f"Enter the BASE event number for subject {subject_base}: ").strip())
    except Exception as e:
        print("Invalid event number. Exiting.")
        return

    # Get the list of compared subject IDs (comma-separated)
    compared_subjects_input = input("Enter the other subject IDs to compare (comma-separated): ").strip()
    compared_subjects = [s.strip() for s in compared_subjects_input.split(",") if s.strip()]
    
    # Get the event numbers (comma-separated) to search for in the compared subjects.
    event_nums_input = input("Enter event numbers for the compared subjects (comma-separated, e.g., 1,2,3): ").strip()
    try:
        compared_events = [int(num.strip()) for num in event_nums_input.split(",") if num.strip()]
    except Exception as e:
        print("Invalid event numbers input. Exiting.")
        return

    # Get the list of activities from the base subject folder.
    base_subject_path = os.path.join(base_path, subject_base)
    if not os.path.isdir(base_subject_path):
        print(f"Base subject folder {subject_base} not found in dataset. Exiting.")
        return

    activities = [a for a in os.listdir(base_subject_path) if os.path.isdir(os.path.join(base_subject_path, a))]
    if not activities:
        print(f"No activity folders found for base subject {subject_base}. Exiting.")
        return

    # Process each activity from the base subject.
    for activity in activities:
        base_activity_path = os.path.join(base_subject_path, activity)
        base_files = glob.glob(os.path.join(base_activity_path, "*.csv"))
        
        # For each sensor file in the base subject that has the given base event number,
        # compare it with the corresponding file(s) from each compared subject.
        for bf in base_files:
            subj, act, sensor, ev = parse_file_info(bf, base_path)
            if ev != base_event or sensor is None:
                continue  # Only process files matching the base event number
            
            base_file = bf  # The file for base subject for this sensor and activity.
            sensor_keyword = sensor  # Using the sensor name as the keyword.
            print(f"Processing activity '{activity}', sensor '{sensor_keyword}' for base subject {subject_base} event {base_event}")

            # For each compared subject, check if the activity folder exists.
            for comp_subj in compared_subjects:
                comp_activity_path = os.path.join(base_path, comp_subj, activity)
                if not os.path.isdir(comp_activity_path):
                    print(f"Activity folder '{activity}' not found for subject {comp_subj}. Skipping.")
                    continue

                # For the current compared subject, gather files matching any of the specified event numbers.
                comparison_files = []
                for comp_ev in compared_events:
                    comp_file = find_event_file(base_path, comp_subj, activity, sensor_keyword, comp_ev)
                    if comp_file:
                        comparison_files.append((comp_subj, comp_ev, comp_file))
                    else:
                        print(f"File not found for subject {comp_subj} in activity {activity} for sensor '{sensor_keyword}' with event {comp_ev}.")
                
                # If we found at least one comparison file for this compared subject, plot the graph.
                if comparison_files:
                    # Destination: dest_base/comp_subj/activity/
                    dest_folder = os.path.join(dest_base, comp_subj, activity)
                    os.makedirs(dest_folder, exist_ok=True)
                    dest_file = os.path.join(dest_folder, f"{subject_base}_{sensor_keyword}_e{base_event}_vs_{comp_subj}_{sensor_keyword}.png")
                    plot_comparison_graph(base_file, comparison_files, sensor_keyword, subject_base, base_event, activity, dest_file)
                else:
                    print(f"No comparison files found for subject {comp_subj} in activity {activity} for sensor '{sensor_keyword}'.")
                
    print("Processing complete.")

if __name__ == "__main__":
    main()
