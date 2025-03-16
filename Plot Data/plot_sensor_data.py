import csv
import matplotlib.pyplot as plt

def load_sensor_data(filepath):
    """
    Loads sensor data from a CSV file.
    
    Expects each row to be either in one of the following formats:
      1. timestamp,x_value,y_value,z_value
      2. timestamp,"x_value, y_value, z_value"
      
    Returns:
      timestamps: list of float timestamps
      x_vals: list of float x-axis sensor values
      y_vals: list of float y-axis sensor values
      z_vals: list of float z-axis sensor values
    """
    timestamps = []
    x_vals = []
    y_vals = []
    z_vals = []
    
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Skip if the row is empty or too short
            if not row or len(row) < 2:
                continue
            
            try:
                # First field should be the timestamp
                ts = float(row[0].strip())
                
                # If the row has 4 fields, assume they are timestamp, x, y, z
                if len(row) >= 4:
                    x = float(row[1].strip())
                    y = float(row[2].strip())
                    z = float(row[3].strip())
                else:
                    # Otherwise, assume row[1] is a string like "x_value, y_value, z_value"
                    sensor_vals = row[1].split(',')
                    if len(sensor_vals) < 3:
                        continue
                    x = float(sensor_vals[0].strip())
                    y = float(sensor_vals[1].strip())
                    z = float(sensor_vals[2].strip())
                    
                timestamps.append(ts)
                x_vals.append(x)
                y_vals.append(y)
                z_vals.append(z)
            except Exception as e:
                print(f"Error processing row {row}: {e}")
                continue
                
    return timestamps[:500], x_vals[:500], y_vals[:500], z_vals[:500]

def plot_sensor_data(timestamps, x_vals, y_vals, z_vals,filepath):
    """
    Plots the sensor data with timestamp on the x-axis and sensor values on the y-axis.
    X, Y, and Z values are shown in different colors.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, x_vals, label='X', color='red', marker='o')
    plt.plot(timestamps, y_vals, label='Y', color='green', marker='o')
    plt.plot(timestamps, z_vals, label='Z', color='blue', marker='o')
    
    plt.xlabel("Timestamp")
    plt.ylabel("Sensor Value")
    plt.title(filepath)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    filepath = input("Enter the full path to the CSV file: ").strip()
    if not filepath:
        print("No file path provided.")
        return

    print("Loading sensor data from file...")
    timestamps, x_vals, y_vals, z_vals = load_sensor_data(filepath)
    
    if not timestamps:
        print("No valid sensor data found in the file.")
        return
    
    print("Plotting sensor data...")
    plot_sensor_data(timestamps, x_vals, y_vals, z_vals,filepath)

if __name__ == "__main__":
    main()
