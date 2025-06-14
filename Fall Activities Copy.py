import os
import shutil

# List of exact fall activity folder names to match
fall_activities = [
    "fall_backward",
    "fall_backward_when_trying_to_sit_down",
    "fall_backward_while_trying_to_sit_down",
    "fall_backward_when_trying_to_stand_up",
    "fall_backward_while_trying_to_stand_up",
    "fall_forward",
    "fall_forward_when_trying_to_sit_down",
    "fall_forward_while_trying_to_sit_down",
    "fall_forward_when_trying_to_stand_up",
    "fall_forward_while_trying_to_stand_up",
    "fall_left",
    "fall_right"
]

def copy_fall_folders(src_root, dest_root):
    if not os.path.exists(src_root):
        print("❌ Source path does not exist.")
        return
    
    # Create destination if it doesn't exist
    if not os.path.exists(dest_root):
        os.makedirs(dest_root)

    # Iterate through each user folder
    for user_folder in os.listdir(src_root):
        user_path = os.path.join(src_root, user_folder)
        
        if os.path.isdir(user_path):
            # Check and create user folder in destination
            dest_user_path = os.path.join(dest_root, user_folder)
            os.makedirs(dest_user_path, exist_ok=True)
            
            # List all subfolders (activities) inside user folder
            for activity_folder in os.listdir(user_path):
                activity_path = os.path.join(user_path, activity_folder)
                
                # Check if it's a folder and matches one of the fall activities
                if os.path.isdir(activity_path) and activity_folder in fall_activities:
                    dest_activity_path = os.path.join(dest_user_path, activity_folder)
                    print(f"📁 Copying {activity_path} to {dest_activity_path}")
                    shutil.copytree(activity_path, dest_activity_path, dirs_exist_ok=True)

    print("✅ Copy operation completed.")

# Main execution
if __name__ == "__main__":
    src = input("Enter the source path (e.g., D://Data/): ").strip()
    dst = input("Enter the destination path to copy fall activities: ").strip()
    copy_fall_folders(src, dst)
