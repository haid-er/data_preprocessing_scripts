import os

def is_standard_subject(name):
    """
    Returns True if the subject folder name is a single word without spaces or underscores.
    """
    return name.islower() and " " not in name and "_" not in name

def rename_subjects(base_path):
    """
    Go through each device folder under base_path. For each subject folder that is not standardized,
    prompt the user for a new subject name (a single word), rename the subject folder, and then
    rename all files in the activity subfolders whose names start with the old subject name.
    """
    # List device folders under the base path.
    device_folders = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    for device in device_folders:
        device_path = os.path.join(base_path, device)
        # List subject folders inside each device folder.
        subject_folders = [s for s in os.listdir(device_path) if os.path.isdir(os.path.join(device_path, s))]
        
        for subject in subject_folders:
            # Skip if the subject folder is already standard.
            if is_standard_subject(subject):
                continue

            subject_path = os.path.join(device_path, subject)
            print(f"\nSubject folder '{subject}' in device '{device}' is not standardized.")
            new_subject = input("Enter the new subject name (a single word in lowercase, e.g., bitf21m541): ").strip().lower()
            while not is_standard_subject(new_subject):
                print("Invalid subject name. It must be a single word without spaces or underscores.")
                new_subject = input("Enter the new subject name: ").strip().lower()

            new_subject_path = os.path.join(device_path, new_subject)
            
            # Rename the subject folder.
            try:
                os.rename(subject_path, new_subject_path)
                print(f"Renamed subject folder '{subject}' to '{new_subject}' in device '{device}'.")
            except Exception as e:
                print(f"Error renaming subject folder '{subject}': {e}")
                continue

            # Now update all files inside every activity folder for this subject.
            # Each subject folder contains one or more activity folders.
            activity_folders = [a for a in os.listdir(new_subject_path) if os.path.isdir(os.path.join(new_subject_path, a))]
            for activity in activity_folders:
                activity_path = os.path.join(new_subject_path, activity)
                # Process each file in the activity folder.
                for file in os.listdir(activity_path):
                    old_file_path = os.path.join(activity_path, file)
                    if os.path.isfile(old_file_path):
                        # If the file name starts with the old subject name, replace it with the new subject name.
                        if file.startswith(subject):
                            new_file_name = new_subject + file[len(subject):]
                            new_file_path = os.path.join(activity_path, new_file_name)
                            try:
                                os.rename(old_file_path, new_file_path)
                                print(f"Renamed file '{file}' to '{new_file_name}' in activity '{activity}' for device '{device}'.")
                            except Exception as e:
                                print(f"Error renaming file '{file}': {e}")

def main():
    base_path = input("Enter the path for Hostel_Data: ").strip()
    if not os.path.exists(base_path):
        print("The specified base path does not exist. Exiting.")
        return

    rename_subjects(base_path)
    print("\nSubject name standardization completed.")

if __name__ == "__main__":
    main()
