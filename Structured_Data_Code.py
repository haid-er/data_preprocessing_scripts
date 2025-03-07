import os
import shutil
import re

def get_existing_devices(base_path):
    """Get the list of existing device folders within the dataset path."""
    devices = {'Smart_Phone': 'phone', 'Smart_Glass': 'glass', 'Smart_Watch': 'watch'}
    existing_devices = {device: short_name for device, short_name in devices.items() if os.path.exists(os.path.join(base_path, device))}
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
    activities = sorted(set.union(*activity_sets))
    return activities

import re

import re

def rename_file(file_name, device):
    """Rename CSV files based on device and sensor type without including the subject name."""
    device_name = device.replace("Smart_", "").lower()

    # Remove any leading subject ID (generic pattern: letters/numbers + _ or -)
    file_name = re.sub(r'^[a-zA-Z0-9]+[_-]+', '', file_name, flags=re.IGNORECASE)
    
    # Remove "Samsung" from the filename
    file_name = re.sub(r'\bSamsung\b', '', file_name, flags=re.IGNORECASE).strip()

    # Sensor name mappings
    sensor_mappings = {
        # Smartphone Sensors
        r"AK09916C Magnetic field Sensor": "magnetometer",
        r"AK09916C Magnetic Sensor UnCalibrated": "magnetometer_uncalibrated",
        r"Gravity Sensor": "gravity",
        r"Interrupt Gyroscope Sensor": "interrupt_gyroscope",
        r"Linear Acceleration Sensor": "linear_acceleration",
        r"LSM6DSL Acceleration Sensor UnCalibrated": "accelerometer",
        r"LSM6DSL Acceleration Sensor": "accelerometer_calibrated",
        r"LSM6DSL Gyroscope sensor UnCalibrated": "gyroscope_uncalibrated",
        r"LSM6DSL Gyroscope Sensor": "gyroscope",
        # Smartwatch Sensors
        r"AK09918C Magnetometer UnCalibrated": "magnetometer_uncalibrated",
        r"AK09918C Magnetometer": "magnetometer",
        r"LSM6DSO Accelerometer": "accelerometer",
        r"LSM6DSO Gyroscope Uncalibrated": "gyroscope_uncalibrated",
        r"LSM6DSO Gyroscope": "gyroscope",
        r"Samsung Linear Acceleration Sensor": "linear_acceleration",
        # Smartglass Sensors
        r"ACCELEROMETER": "accelerometer",
        r"GYROSCOPE": "gyroscope",
        r"Magnetometer": "magnetometer"
    }

    # Apply sensor name replacements (case-insensitive)
    for key, value in sensor_mappings.items():
        file_name = re.sub(key, value, file_name, flags=re.IGNORECASE)

    # Ensure consistent formatting
    new_name = f"{device_name}_{file_name}".replace(" ", "_")

    # Ensure .csv extension
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
        
        for device, short_device in existing_devices.items():
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
            print(f"Available activities for subject '{subject}':", activities + ["ALL"])
            activity_choice = input(f"Enter an activity name or 'ALL' to copy all for '{subject}': ").strip().lower()
            
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
        subject_input = input("Enter a subject ID or 'ALL' to select all: ").strip().lower()
        
        if subject_input == "all":
            selected_subjects = list(original_subjects.values())
            break
        elif subject_input in common_subjects:
            selected_subjects = [original_subjects[subject_input]]
            break
        else:
            print("Invalid subject. Please choose from the list.")
    
    save_path = input("Enter the path to save structured data: ").strip()
    os.makedirs(save_path, exist_ok=True)
    
    create_hierarchy(base_path, selected_subjects, save_path, existing_devices)

if __name__ == "__main__":
    main()