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

def clean_filename(file_name):
    """Remove redundant patterns like '_eX.csv_eX.csv'."""
    # Regular expression to match patterns like '_eX.csv_eX.csv'
    cleaned_name = re.sub(r'(_e\d+\.csv)_e\d+\.csv$', r'\1', file_name)
    return cleaned_name

def rename_file(file_name, device):
    """Rename CSV files based on device and sensor type without including the subject name."""
    device_name = device.replace("Smart_", "").lower()
    parts = re.split(r'[_ ]', file_name)
    
    sensor_type = ""
    extra_info = ""
    sequence = ""
    
    if device == "Smart_Glass":
        if len(parts) == 2 and parts[1].lower() in ["gyroscope", "magnetometer", "gravity"]:
            sensor_type = parts[1].lower()
            if sensor_type == "gravity":
                sensor_type = "gravity_sensor"
            new_name = f"{device_name}_{sensor_type}"
        elif len(parts) >= 3:
            sensor_type = parts[1].lower()
            extra_info = parts[2].lower()
            for part in reversed(parts):
                if part.startswith('e'):
                    sequence = part[1:]
                    break
            new_name = f"{device_name}_{sensor_type}_{extra_info}_e{sequence}" if sequence else f"{device_name}_{sensor_type}_{extra_info}"
        else:
            new_name = f"{device_name}_{file_name}"
    else:
        if len(parts) >= 4:
            sensor_type = parts[2].lower().replace(" ", "_")
            extra_info = parts[3].lower().replace(" ", "_")
            for part in reversed(parts):
                if part.startswith('e'):
                    sequence = part[1:]
                    break
            new_name = f"{device_name}_{sensor_type}_{extra_info}_e{sequence}" if sequence else f"{device_name}_{sensor_type}_{extra_info}"
        elif len(parts) >= 3:
            sensor_type = parts[2].lower().replace(" ", "_")
            for part in reversed(parts):
                if part.startswith('e'):
                    sequence = part[1:]
                    break
            new_name = f"{device_name}_{sensor_type}_e{sequence}" if sequence else f"{device_name}_{sensor_type}"
        else:
            new_name = f"{device_name}_{file_name}"
    
    sensor_names = ["accelerometer", "gyroscope", "magnetometer", "linear acceleration", "gravity", "magnetic", "acceleration"]
    for sensor_name in sensor_names:
        match = re.search(sensor_name, file_name, re.IGNORECASE)
        if match:
            new_name = new_name.replace(sensor_type, sensor_name.lower().replace(" ", "_")) if sensor_type else f"{device_name}_{sensor_name.lower().replace(' ', '_')}"
            break

    if "magnetic field" in file_name.lower():
        new_name = new_name.replace("magnetic_field", "magnetometer")
    if "gravity_sensor" in file_name.lower():
        new_name = new_name.replace("gravity_sensor", "gravity")
    if "linear_acceleration" in new_name:
        new_name = new_name.replace("linear_acceleration", "linear_accelerometer")

    new_name = clean_filename(new_name)

    if not new_name.endswith(".csv"):
        new_name += ".csv"
    
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
                selected_activities = [a for a in activities if a.lower() == activity_choice]
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
    os.makedirs(save_path, exist_ok=True)

    create_hierarchy(base_path, selected_subjects, save_path, existing_devices)

if __name__ == "__main__":
    main()
