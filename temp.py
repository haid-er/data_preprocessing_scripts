import os

# Specify the folder path
folder_path = r'C:\Users\Malik Haider\Documents\NewHumCare\DS_Structured\bsef21m542\downstairs'  # Change this to your actual path

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if 'event_' in filename:
        new_filename = filename.replace('event_', '')
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)
        
        os.rename(old_file_path, new_file_path)
        print(f'Renamed: {filename} → {new_filename}')


# import os
# import re

# folder_path = r'C:\Users\Malik Haider\Documents\NewHumCare\DS_Structured\msdsf23m015\downstairs'  # Change to your actual folder path

# def get_max_index(prefix):
#     max_index = -1
#     for f in os.listdir(folder_path):
#         if f.startswith(prefix) and re.search(r'_e(\d+)\.csv$', f):
#             num = int(re.search(r'_e(\d+)\.csv$', f).group(1))
#             max_index = max(max_index, num)
#     return max_index

# def rename_files(prefix):
#     max_index = get_max_index(prefix)
#     for f in os.listdir(folder_path):
#         if f.startswith(prefix) and re.search(r'_e\d+_e\d+\.csv$', f):
#             old_path = os.path.join(folder_path, f)
#             max_index += 1
#             new_name = f"{prefix}_e{max_index}.csv"
#             new_path = os.path.join(folder_path, new_name)
#             os.rename(old_path, new_path)
#             print(f"Renamed: {f} → {new_name}")

# # Rename for both sensors
# rename_files('glass_accelerometer')
# rename_files('glass_gyroscope')
# rename_files('glass_magnetometer')
# rename_files('phone_magnetometer')
# rename_files('watch_magnetometer')
# rename_files('phone_accelerometer')
# rename_files('watch_accelerometer')
# rename_files('phone_gyroscope')
# rename_files('watch_gyroscope')
