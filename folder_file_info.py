# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 00:01:21 2024

@author: sijian
"""

import os
import pandas as pd

def get_file_info(file_path):
    name, extension = os.path.splitext(file_path)
    return {
        'path': file_path,
        'name': os.path.basename(name),
        'extension': extension,
        'directory': os.path.isdir(file_path),
        'size': os.path.getsize(file_path) if os.path.isfile(file_path) else None
    }

def explore_folder(folder_path):
    data = []
    for root, dirs, files in os.walk(folder_path):
        for file in files + dirs:
            file_path = os.path.join(root, file)
            data.append(get_file_info(file_path))
    return data

def create_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    folder_path = r"H:\software"  # Replace with the path to your folder
    output_file = "file_info.xlsx"  # Output Excel file

    file_info_data = explore_folder(folder_path)
    create_excel(file_info_data, output_file)

    print(f"File information exported to {output_file}")
