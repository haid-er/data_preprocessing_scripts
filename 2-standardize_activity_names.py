import os

# Standard activity names (all in lowercase)
STANDARD_ACTIVITIES = [
    "bending",
    "walking",
    "standing_up_from_sitting",
    "sitting_down_from_standing",
    "slow_walk",
    "squatting",
    "open_door",
    "close_door",
    "quick_walk",
    "sitting",
    "put_on_floor",
    "pick_from_floor",
    "laying_down_from_sitting",
    "standing_up_from_laying",
    "typing",
    "jogging",
    "clean_the_table",
    "open_bag",
    "open_big_box",
    "reading",
    "close_lid_by_rotation",
    "plugin",
    "throw_out",
    "laying",
    "eat_small_things",
    "talk_using_phone",
    "standing",
    "upstairs",
    "downstairs",
    "drink_water",
    "fall_forward",
    "fall_right",
    "fall_backward",
    "fall_left",
    "fall_forward_when_trying_to_sit_down",
    "fall_backward_while_trying_to_sit_down",
    "fall_forward_while_trying_to_stand_up",
    "fall_backward_while_trying_to_stand_up",
    "open_lid_by_rotation"
]

def standardize_activity_names(base_path):
    """
    This function goes through each device folder (inside the base path), then through each subject folder,
    and finally each activity folder. If the activity folder's name (lowercased) is not in the standard list,
    it will prompt the user for the correct standardized name. The mapping is cached so that the same non-standard
    name is only prompted once. It also handles merging if a folder with the target name already exists.
    """
    # Dictionary to store mappings from non-standard to standard names.
    mapping = {}

    # Assume that device folders are immediate subdirectories of base_path.
    devices = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    for device in devices:
        device_path = os.path.join(base_path, device)
        # Get subject folders within each device folder.
        subjects = [s for s in os.listdir(device_path) if os.path.isdir(os.path.join(device_path, s))]
        for subject in subjects:
            subject_path = os.path.join(device_path, subject)
            # Get activity folders within the subject folder.
            activities = [a for a in os.listdir(subject_path) if os.path.isdir(os.path.join(subject_path, a))]
            for activity in activities:
                act_lower = activity.lower()
                # If already standard, nothing to do.
                if act_lower in STANDARD_ACTIVITIES:
                    continue

                # If we have seen this non-standard activity before, reuse the mapping.
                if act_lower in mapping:
                    new_name = mapping[act_lower]
                else:
                    # Prompt the user for a mapping.
                    print(f"\nFound non-standard activity folder: '{activity}' in {subject_path}")
                    print("Standard activity names are:")
                    for act in STANDARD_ACTIVITIES:
                        print(f" - {act}")
                    new_name = input(f"Enter the standardized name for '{activity}': ").strip().lower()
                    # Continue prompting until a valid standard name is entered.
                    while new_name not in STANDARD_ACTIVITIES:
                        print("Invalid input. Please enter one of the standard activity names exactly as shown above.")
                        new_name = input(f"Enter the standardized name for '{activity}': ").strip().lower()
                    mapping[act_lower] = new_name

                # Build the full paths.
                old_folder_path = os.path.join(subject_path, activity)
                new_folder_path = os.path.join(subject_path, new_name)

                # If a folder with the standardized name already exists, merge the contents.
                if os.path.exists(new_folder_path):
                    print(f"Folder '{new_folder_path}' already exists. Merging contents from '{old_folder_path}'.")
                    for item in os.listdir(old_folder_path):
                        src = os.path.join(old_folder_path, item)
                        dst = os.path.join(new_folder_path, item)
                        # If there is a name conflict, you can choose to skip or rename the file.
                        if os.path.exists(dst):
                            print(f"File '{dst}' already exists; skipping it.")
                        else:
                            os.rename(src, dst)
                    try:
                        os.rmdir(old_folder_path)
                        print(f"Removed empty folder '{old_folder_path}'.")
                    except Exception as e:
                        print(f"Could not remove folder '{old_folder_path}': {e}")
                else:
                    os.rename(old_folder_path, new_folder_path)
                    print(f"Renamed '{old_folder_path}' to '{new_folder_path}'.")

    print("\nAll activity folder names have been standardized.")

def main():
    base_path = input("Enter the base path for the dataset: ").strip()
    if not os.path.exists(base_path):
        print("The specified base path does not exist. Exiting.")
        return

    standardize_activity_names(base_path)

if __name__ == "__main__":
    main()
