# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 22:52:14 2024

@author: sijian
"""

import shutil
import os
import datetime
import filecmp


def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Successfully deleted the folder: '{folder_path}'.")
    except Exception as e:
        print(f"Error: {e}")
 

def copy_folder(source_folder, destination_folder):
    try:
        shutil.copytree(source_folder, destination_folder, symlinks=True)
        print(f"Successfully copied from '{source_folder}' to '{destination_folder}'.")
    except Exception as e:
        print(f"Error: {e}")

# folder_to_delete = r'I:\software'  
# delete_folder(folder_to_delete)
    

# folder_ls = [r'\documents',r'\image',r'software']

# source_drive = r'H:'
# destination_drive = r'I:'

# source_path_ls = [os.path.join(source_drive,folder) for folder in folder_ls]
# destination_path_ls = [os.path.join(destination_drive,folder) for folder in folder_ls]

# for i in range(len(source_path_ls)):
    
#     a = datetime.datetime.now()
#     print('Copying path: from {} to {}'.format(source_path_ls[i], destination_path_ls[i]))
#     print('Start time: {}'.format(a))
    
#     copy_folder(source_path_ls[i], destination_path_ls[i])
    
#     b = datetime.datetime.now()
#     print('Path copy finished: from {} to {}'.format(source_path_ls[i], destination_path_ls[i]))
#     print('End time: {}'.format(b))
#     # print('Time used: ()')
#     # Calculate time difference
#     time_difference = b - a
    
#     # Extract minutes and seconds from the timedelta
#     minutes, seconds = divmod(time_difference.seconds, 60)
    
#     # Format the result string
#     result_string = f'Time Used: {minutes} min {seconds} seconds'
    
#     print(result_string)


def synchronize_folders(source_folder, destination_folder):
    # print(f"Starting to sync '{source_folder}' to '{destination_folder}'")
    dcmp = filecmp.dircmp(source_folder, destination_folder)

    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Copy new and modified files from source to destination
    for file in dcmp.diff_files + dcmp.left_only:
        source_path = os.path.join(source_folder, file)
        destination_path = os.path.join(destination_folder, file)

        if os.path.isdir(source_path):
            # Recursive call for subdirectories
            synchronize_folders(source_path, destination_path)
        else:
            shutil.copy2(source_path, destination_path)
            print(f"Copied: file '{file}' from '{source_folder}' to '{destination_folder}'")

    # Delete files and directories in destination that are not in source
    for file in dcmp.right_only:
        file_path = os.path.join(destination_folder, file)

        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
            print(f"Deleted: directory '{file}' from '{destination_folder}'")
        else:
            os.remove(file_path)
            print(f"Deleted: file '{file}' from '{destination_folder}'")
        
        # print(f"Deleted: {file}")

    # Recursive synchronization for common subdirectories
    for subfolder in dcmp.common_dirs:
        synchronize_folders(
            os.path.join(source_folder, subfolder),
            os.path.join(destination_folder, subfolder)
        )


folder_B = r'H:\image'  # Replace with the path to folder A
folder_A = r'I:\image'  # Replace with the path to folder B

synchronize_folders(folder_A, folder_B)
