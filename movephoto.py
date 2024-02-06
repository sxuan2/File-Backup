# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 21:38:06 2023

@author: sijian
"""

import os
import shutil
from datetime import datetime

# os.chdir(r'H:\image\photo_input')



input_folder = r'H:\image\photo_input'
input_folder2 = r'H:\image\photo_input_staging'
output_path = r'H:\image\PhotoOutput'
file_ls = os.listdir(input_folder2)
foldername_ls=['2016','2017','2018','2019','2020','2021','2022','2023','2024']



def get_earliest_date(file_path):
    # Get the earliest date among creation and modification
    created_time = os.path.getctime(file_path)
    modified_time = os.path.getmtime(file_path)
    return min(created_time, modified_time)

# test = get_earliest_date(r'H:\image\New folder\mmexport1660052019881.jpg')
# formatted_date = datetime.utcfromtimestamp(test).strftime('%Y-%m-%d-%H_%M_%S')
# print(formatted_date)

def rename_image_with_earliest_date(file_path,input_folder2):
    # Get the earliest date
    earliest_date = get_earliest_date(file_path)
    
    # Format the date as a string (you can customize the format)
    formatted_date = datetime.utcfromtimestamp(earliest_date).strftime('%Y-%m-%d-%H_%M_%S')

    # Extract the file extension
    _, file_extension = os.path.splitext(file_path)

    # Create the new file name with the earliest date
    new_file_name = os.path.join(input_folder2,formatted_date + file_extension)

    # Move the file (across drives if necessary)
    shutil.move(file_path, new_file_name)
    # print(file_path)
    # print(new_file_name)
    print(f'Renamed "{file_path}" to "{new_file_name}" with earliest date {formatted_date}')

# rename_image_with_earliest_date(os.path.join(input_folder,'mmexport1660052019881.jpg'),input_folder2=input_folder2)

def rename_images_in_folder(folder_path,input_folder2):
    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Check if the file is an image (you can customize the list of allowed extensions)
        if os.path.isfile(file_path) and file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4','.mov')):
            rename_image_with_earliest_date(file_path,input_folder2)
        elif os.path.isfile(file_path):
            print(f'Skipping non-image file: {file_path}')

# Rename images in the folder
rename_images_in_folder(input_folder,input_folder2)




for foldername in foldername_ls:
    for file in file_ls:
        # if foldername in file:
        if file[:4] == foldername:
            if not os.path.exists(os.path.join(output_path,foldername)):
            	os.mkdir(os.path.join(output_path,foldername))
            	shutil.move(os.path.join(input_folder2,file),os.path.join(output_path,foldername,file))
            else:
            	shutil.move(os.path.join(input_folder2,file),os.path.join(output_path,foldername,file))
                
                
                