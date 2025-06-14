import os

# Define renaming rules (modify as needed)
rename_mapping = {
    "downstair": "downstairs",
    "sitting_down_from_standing": "sit_down",
    "sitting_down": "sit_down",
    "standing_up_from_laying": "sufl",
    "standing_up_from_sitting": "sufs",
    "upstair": "upstairs"
}

def rename_activity_folders(main_folder):
    if not os.path.exists(main_folder):
        print("Invalid path! Please enter a correct directory.")
        return

    total_subjects = 0
    total_renamed = 0
    total_skipped = 0

    # Iterate over subject folders
    for subject in os.listdir(main_folder):
        subject_path = os.path.join(main_folder, subject)

        if os.path.isdir(subject_path):  # Ensure it's a folder
            total_subjects += 1
            renamed_count = 0
            skipped_count = 0

            print(f"\n📂 Processing subject: {subject}")

            for item in os.listdir(subject_path):
                item_path = os.path.join(subject_path, item)

                # Skip files and non-folder items
                if not os.path.isdir(item_path):
                    print(f"📄 Skipping file: {item}")
                    continue  

                # Rename only folders that match the mapping
                new_name = rename_mapping.get(item, None)

                if new_name:
                    new_path = os.path.join(subject_path, new_name)
                    os.rename(item_path, new_path)
                    print(f"🚀🚀🚀🚀🚀🚀Renamed: {item} ➝ {new_name}")
                    renamed_count += 1
                else:
                    print(f"Skipped: {item} (No match found)")
                    skipped_count += 1

            # Show statistics for this subject
            print(f"📊 Summary for {subject}: Renamed: {renamed_count}, Skipped: {skipped_count}")

            total_renamed += renamed_count
            total_skipped += skipped_count

    # Final summary
    print("\n📌 Final Summary:")
    print(f"✅ Total Subjects Processed: {total_subjects}")
    print(f"🔄 Total Activities Renamed: {total_renamed}")
    print(f"⏭️ Total Activities Skipped: {total_skipped}")

if __name__ == "__main__":
    main_folder = input("Enter the path to the main folder (e.g., D:\Synchronized Data): ").strip()
    rename_activity_folders(main_folder)
