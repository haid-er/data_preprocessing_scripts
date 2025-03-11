#!/usr/bin/env python3
import argparse
import pandas as pd
import math

def read_sensor_file(filepath, col_names):
    """
    Reads a CSV file using only the first four columns and renames them.
    Expected order: timestamp, valueX, valueY, valueZ.
    """
    df = pd.read_csv(filepath, usecols=[0, 1, 2, 3])
    df = df.iloc[:, :4]
    df.columns = col_names
    # Convert timestamp to float (timestamps are assumed to be in milliseconds)
    df[col_names[0]] = pd.to_numeric(df[col_names[0]], errors='coerce')
    return df

def compute_gravity_fusion(df, alpha=0.98, G=13.25):
    """
    Computes gravity using sensor fusion (accelerometer, gyroscope, and magnetometer).
    
    Parameters:
      df: DataFrame with merged sensor data containing columns:
          ['timestamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz']
      alpha: Complementary filter coefficient (0 < alpha < 1).
      G: Gravitational constant (set to match the gravity sensor calibration; here ≈13.25).
    
    Returns:
      List of computed values: [timestamp, gravity_x, gravity_y, gravity_z]
    
    Formula:
      From accelerometer:
         roll_acc  = atan2(a_y, a_z)
         pitch_acc = atan2(-a_x, sqrt(a_y² + a_z²))
      
      Integrate gyroscope (convert deg/s to rad/s if needed):
         roll_gyro  = previous_roll + (gx_rad * dt)
         pitch_gyro = previous_pitch + (gy_rad * dt)
      
      Complementary filter:
         roll  = alpha * roll_gyro  + (1 - alpha) * roll_acc
         pitch = alpha * pitch_gyro + (1 - alpha) * pitch_acc
      
      Compute gravity vector:
         gₓ = -G * sin(pitch)
         g_y =  G * sin(roll) * cos(pitch)
         g_z =  G * cos(roll) * cos(pitch)
    """
    # Initialize previous angles (assumed starting from 0)
    prev_roll = 0.0
    prev_pitch = 0.0
    gravity_values = []
    
    # Use the first timestamp as reference; note timestamps are in ms.
    prev_time = df.iloc[0]['timestamp']

    # Process each row
    for index, row in df.iterrows():
        current_time = row['timestamp']
        # Compute time difference in seconds (timestamps are in milliseconds)
        dt = (current_time - prev_time) / 1000.0 if index > 0 else 0.0
        
        # Read accelerometer data
        ax, ay, az = row['ax'], row['ay'], row['az']
        
        # Compute accelerometer-based estimates of roll and pitch:
        roll_acc  = math.atan2(ay, az)
        pitch_acc = math.atan2(-ax, math.sqrt(ay**2 + az**2))
        
        # Read gyroscope data (assumed to be in deg/s; convert to rad/s)
        gx, gy, _ = row['gx'], row['gy'], row['gz']
        gx_rad = math.radians(gx)
        gy_rad = math.radians(gy)
        
        # Integrate gyroscope data to get angles:
        roll_gyro  = prev_roll + gx_rad * dt
        pitch_gyro = prev_pitch + gy_rad * dt
        
        # Apply complementary filter:
        roll  = alpha * roll_gyro  + (1 - alpha) * roll_acc
        pitch = alpha * pitch_gyro + (1 - alpha) * pitch_acc

        # (Optionally, one could compute yaw using the magnetometer; omitted here because gravity depends on roll and pitch.)
        
        # Compute gravity vector using the fused angles:
        g_x = -G * math.sin(pitch)
        g_y =  G * math.sin(roll) * math.cos(pitch)
        g_z =  G * math.cos(roll) * math.cos(pitch)
        
        gravity_values.append([current_time, g_x, g_y, g_z])
        
        # Update previous angles and timestamp
        prev_roll = roll
        prev_pitch = pitch
        prev_time = current_time
        
    return gravity_values

def main():
    parser = argparse.ArgumentParser(
        description="Compute gravity vector from sensor fusion of accelerometer, gyroscope, and magnetometer data.\n"
                    "The CSV files must have at least four columns: timestamp, X, Y, Z (extra columns are ignored)."
    )
    parser.add_argument("acc_file", help="Path to the accelerometer CSV file")
    parser.add_argument("gyro_file", help="Path to the gyroscope CSV file")
    parser.add_argument("mag_file", help="Path to the magnetometer CSV file")
    parser.add_argument("--output", default="computed_gravity.csv", help="Output CSV file name")
    parser.add_argument("--alpha", type=float, default=0.98, help="Complementary filter coefficient (default: 0.98)")
    # Optionally, one could allow the gravitational constant to be adjusted
    parser.add_argument("--G", type=float, default=13.25, help="Gravitational constant to use (default: 13.25)")
    args = parser.parse_args()
    
    # Read sensor CSV files (using only the first four columns)
    df_acc = read_sensor_file(args.acc_file, ['timestamp', 'ax', 'ay', 'az'])
    df_gyro = read_sensor_file(args.gyro_file, ['timestamp', 'gx', 'gy', 'gz'])
    df_mag = read_sensor_file(args.mag_file, ['timestamp', 'mx', 'my', 'mz'])
    
    # Merge data on timestamp (assuming time-synchronization)
    df_merge = pd.merge(df_acc, df_gyro, on='timestamp')
    df_merge = pd.merge(df_merge, df_mag, on='timestamp')
    
    # Compute gravity vector using the complementary filter fusion
    gravity_values = compute_gravity_fusion(df_merge, alpha=args.alpha, G=args.G)
    
    # Save the computed gravity values to CSV
    df_out = pd.DataFrame(gravity_values, columns=['timestamp', 'gravity_x', 'gravity_y', 'gravity_z'])
    df_out.to_csv(args.output, index=False)
    print(f"Computed gravity vector saved to {args.output}")

if __name__ == "__main__":
    main()
