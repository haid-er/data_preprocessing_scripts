import os
import re
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def clean_filename(file_name):
    """
    Remove redundant patterns like '_eX.csv_eX.csv' from the filename.
    """
    cleaned_name = re.sub(r'(_e\d+\.csv)_e\d+\.csv$', r'\1', file_name)
    return cleaned_name

def parse_file_info(file_path, base_path):
    """
    Extract subject, activity, sensor name, and event number from file path.
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
        sensor = match.group(1)  # Extract sensor name
        event_num = int(match.group(2))  # Extract event number
    else:
        sensor, event_num = None, None
    return subject, activity, sensor, event_num

def plot_event_files(file_paths, dest_base, base_path):
    """
    Reads multiple CSV files for the same activity and sensor, 
    plots the 'x' values from each event in a single graph, 
    and saves the graph in the destination folder.
    """
    x_columns = []
    labels = []
    
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path, delimiter=",", header=None)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

        # Assign column names assuming at least 4 columns exist
        if df.shape[1] >= 4:
            df = df.iloc[:, :4]  # Use only the first 4 columns
            df.columns = ['timestamp', 'x', 'y', 'z']
        else:
            df.columns = ['x', 'y', 'z']

        # Extract event number from file name
        _, _, _, event_num = parse_file_info(file_path, base_path)
        if event_num is None:
            print(f"Skipping {file_path} due to missing event number.")
            continue

        x_columns.append(df['x'])
        labels.append(f"e{event_num}")

    if not x_columns:
        print("No valid data found for plotting.")
        return

    # Plot all event data on the same graph
    plt.figure(figsize=(10, 6))
    for i, x_data in enumerate(x_columns):
        plt.plot(x_data.values, label=labels[i])

    subject, activity, sensor, _ = parse_file_info(file_paths[0], base_path)
    plt.title(f"{subject} - {activity} - {sensor} (X-axis)")
    plt.xlabel("Time (samples)")
    plt.ylabel("X Value")
    plt.legend()
    plt.grid(True)

    # Save the plot
    rel_folder = os.path.relpath(os.path.dirname(file_paths[0]), base_path)
    dest_folder = os.path.join(dest_base, rel_folder)
    os.makedirs(dest_folder, exist_ok=True)

    dest_file = os.path.join(dest_folder, f"{sensor}_x_axis_plot.png")
    plt.savefig(dest_file)
    plt.close()
    print(f"Saved graph: {dest_file}")

def main():
    # Prompt for the source structured data folder
    source_dir = input("Enter the path to the structured data folder: ").strip()
    while not os.path.exists(source_dir):
        print("Path does not exist.")
        source_dir = input("Enter the path to the structured data folder: ").strip()

    # Prompt for the destination folder for graphs
    dest_dir = input("Enter the destination path for plotted graphs: ").strip()
    os.makedirs(dest_dir, exist_ok=True)

    # Traverse the hierarchy to collect event files by sensor
    file_groups = {}  # Dictionary to store files grouped by (subject, activity, sensor)

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.csv'):
                file_path = os.path.join(root, file)
                subject, activity, sensor, event_num = parse_file_info(file_path, source_dir)
                if None in (subject, activity, sensor, event_num):
                    continue

                key = (subject, activity, sensor)
                if key not in file_groups:
                    file_groups[key] = []
                file_groups[key].append(file_path)

    # Process each group of files and plot
    for key, file_paths in file_groups.items():
        plot_event_files(sorted(file_paths), dest_dir, source_dir)

if __name__ == "__main__":
    main()