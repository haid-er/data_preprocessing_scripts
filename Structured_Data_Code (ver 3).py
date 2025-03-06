import os
import shutil
import re

def get_existing_devices(base_path):
    """Get the list of existing device folders within the dataset path."""
    devices = ['Smart_Phone', 'Smart_Glass', 'Smart_Watch']
    existing_devices = [device for device in devices if os.path.exists(os.path.join(base_path, device))]
    return existing_devices

def get_common_subjects(base_path, existing_devices):
    """Get common user IDs present in all available device folders in real-time, case-insensitive."""
    subject_sets = [set(map(str.lower, os.listdir(os.path.join(base_path, device)))) for device in existing_devices if os.path.exists(os.path.join(base_path, device))]
    if not subject_sets:
        return [], {}
    common_subjects = sorted(set.intersection(*subject_sets))
    
    original_subjects = {}
    for device in existing_devices:
        for subj in os.listdir(os.path.join(base_path, device)):
            if subj.lower() in common_subjects:
                original_subjects[subj.lower()] = subj  # Store original case
    
    return common_subjects, original_subjects

def get_activities_for_subject(base_path, subject, existing_devices):
    """Get activities for the selected subject across all available devices."""
    activity_sets = [set(os.listdir(os.path.join(base_path, device, subject))) for device in existing_devices if os.path.exists(os.path.join(base_path, device, subject))]
    if not activity_sets:
        return []
    activities = sorted(set.union(*activity_sets))  # Use union to get all activities for the subject
    return activities

def rename_file(file_name, device):
    """Rename CSV files based on device and sensor type without including the subject name."""
    # Remove "Smart_" from the device name
    device_name = device.replace("Smart_", "").lower()
    
    # Split the file name by underscores and spaces to extract sensor type and extra info
    parts = re.split(r'[_ ]', file_name)
    
    # Handle different formats
    sensor_type = ""
    extra_info = ""
    sequence = ""
    
    if device == "Smart_Glass":
        if len(parts) == 2 and parts[1].lower() in ["gyroscope", "magnetometer", "gravity"]:
            sensor_type = parts[1].lower()
            if sensor_type == "gravity":
                sensor_type = "gravity_sensor"
            sequence = ""
            new_name = f"{device_name}_{sensor_type}"
        elif len(parts) >= 3:
            sensor_type = parts[1].lower()
            extra_info = parts[2].lower()
            
            # Extract the sequence number
            for part in reversed(parts):
                if part.startswith('e'):
                    sequence = part[1:]
                    break
            
            # Construct the new file name
            if sequence:
                new_name = f"{device_name}_{sensor_type}_{extra_info}_e{sequence}"
            else:
                new_name = f"{device_name}_{sensor_type}_{extra_info}"
        else:
            new_name = f"{device_name}_{file_name}"
    else:
        if len(parts) >= 4:  # Check if there are enough parts
            sensor_type = parts[2].lower().replace(" ", "_")
            extra_info = parts[3].lower().replace(" ", "_")
            
            # Extract the sequence number
            for part in reversed(parts):
                if part.startswith('e'):
                    sequence = part[1:]
                    break
            
            # Construct the new file name
            if sequence:
                new_name = f"{device_name}_{sensor_type}_{extra_info}_e{sequence}"
            else:
                new_name = f"{device_name}_{sensor_type}_{extra_info}"
        elif len(parts) >= 3:  # If there's only a sensor type
            sensor_type = parts[2].lower().replace(" ", "_")
            
            # Extract the sequence number
            for part in reversed(parts):
                if part.startswith('e'):
                    sequence = part[1:]
                    break
            
            # Construct the new file name
            if sequence:
                new_name = f"{device_name}_{sensor_type}_e{sequence}"
            else:
                new_name = f"{device_name}_{sensor_type}"
        else:  # If the file name structure is unexpected
            new_name = f"{device_name}_{file_name}"
    
    # Use regular expression to extract sensor name
    sensor_names = ["accelerometer", "gyroscope", "magnetometer", "linear acceleration", "gravity", "magnetic", "acceleration"]
    for sensor_name in sensor_names:
        match = re.search(sensor_name, file_name, re.IGNORECASE)
        if match:
            if sensor_type:  # Check if sensor_type is defined
                new_name = new_name.replace(sensor_type, sensor_name.lower().replace(" ", "_"))
            else:
                new_name = f"{device_name}_{sensor_name.lower().replace(' ', '_')}"
            break
    
    # Handle "magnetic field" and "uncalibrated" cases
    if "magnetic field" in file_name.lower():
        new_name = new_name.replace("magnetic_field", "magnetometer")
    if "gravity_sensor" in file_name.lower():
        new_name = new_name.replace("gravity_sensor", "gravity")
    if "magnetic" in file_name.lower():
        new_name = new_name.replace("magnetic", "magnetometer")
    if "acceleration" in file_name.lower():
        new_name = new_name.replace("acceleration", "accelerometer")
    if "linear_accelerometer_acceleration" in new_name:
        new_name = new_name.replace("linear_accelerometer_acceleration", "linear_accelerometer")
    if "linear_accelerometer_accelerometer" in new_name:
        new_name = new_name.replace("linear_accelerometer_accelerometer", "linear_accelerometer")
    if "magnetometer uncalibrated" in new_name:
        new_name = new_name.replace("magnetometer uncalibrated", "magnetometer_uncalibrated")
    elif "uncalibrated" in new_name:
        new_name = new_name.replace("uncalibrated", "uncalibrated")
    
    # Handle "linear acceleration" to "linear_accelerometer"
    if "linear_acceleration" in new_name:
        new_name = new_name.replace("linear_acceleration", "linear_accelerometer")
    
    # Handle "gravity" to "gravity_sensor"
    if "gravity" in new_name:
        new_name = new_name.replace("gravity", "gravity_sensor")
    
    # Remove "sensor" from the file name if not needed
    if "gravity_sensor" in new_name:
        pass
    else:
        new_name = new_name.replace("_sensor", "").replace("sensor_", "").replace("sensor", "")
    
    # Remove any extra .csv if present
    if new_name.endswith(".csv"):
        new_name = new_name[:-4]
    
    # Remove any extra _eX after .csv
    if ".csv" in new_name:
        parts = new_name.split(".csv")
        if len(parts) > 1 and parts[1].startswith("_e"):
            new_name = parts[0]
    
    return new_name


def copy_files(base_path, subject, activities, save_path, existing_devices):
    """Copy and rename CSV files while maintaining the correct structure."""
    subject_folder = os.path.join(save_path, subject)
    os.makedirs(subject_folder, exist_ok=True)
    
    for activity in activities:
        activity_folder = os.path.join(subject_folder, activity)
        os.makedirs(activity_folder, exist_ok=True)
        
        for device in existing_devices:
            old_activity_path = os.path.join(base_path, device, subject, activity)
            if os.path.exists(old_activity_path):
                for file in os.listdir(old_activity_path):
                    if file.endswith('.csv'):
                        new_file_name = rename_file(file, device)
                        # Add .csv extension if it's missing
                        if not new_file_name.endswith('.csv'):
                            new_file_name += '.csv'
                        shutil.copy(os.path.join(old_activity_path, file), os.path.join(activity_folder, new_file_name))
        print(f"CSV files copied successfully for activity '{activity}'!")

def create_hierarchy(base_path, subjects, save_path, existing_devices):
    """Create the directory structure and copy all selected activities for each subject."""
    for subject in subjects:
        activities = get_activities_for_subject(base_path, subject, existing_devices)
        if not activities:
            print(f"No activities found for subject '{subject}'.")
            continue
        
        while True:
            print("Available activities for subject '{}':".format(subject), activities + ["ALL"])
            activity_choice = input("Enter the activity name from the list or type 'ALL' to copy all activities for subject '{}': ".format(subject)).strip().lower()
            
            if activity_choice == "all":
                selected_activities = activities
                break
            elif activity_choice in [a.lower() for a in activities]:
                selected_activities = [a for a in activities if a.lower() == activity_choice][0]
                break
            else:
                print("Invalid activity. Please choose from the list.")
        
        copy_files(base_path, subject, selected_activities, save_path, existing_devices)

def main():
    base_path = input("Enter the path to the dataset folder: ").strip()
    while not os.path.exists(base_path):
        print("Invalid path. Please try again.")
        base_path = input("Enter the path to the dataset folder: ").strip()
    
    existing_devices = get_existing_devices(base_path)
    if not existing_devices:
        print("No valid device folders found in the dataset path.")
        return
    
    common_subjects, original_subjects = get_common_subjects(base_path, existing_devices)
    if not common_subjects:
        print("No common subjects found across available devices.")
        return
    
    while True:
        print("Available subjects:", list(original_subjects.values()) + ["ALL"])
        subject_input = input("Enter the subject ID from the list or type 'ALL' to select all subjects: ").strip().lower()
        
        if subject_input == "all":
            selected_subjects = list(original_subjects.values())
            break
        elif subject_input in common_subjects:
            selected_subjects = [original_subjects[subject_input]]
            break
        else:
            print("Invalid subject. Please choose from the list.")
    
    save_path = input("Enter the path where you want to save the structured data: ").strip()
    while not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    
    create_hierarchy(base_path, selected_subjects, save_path, existing_devices)

if __name__ == "__main__":
    main()