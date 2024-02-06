# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 19:14:14 2024

@author: sijian
"""


# backup plan


import shutil
import os
import datetime
import filecmp

import wx


class FolderSyncApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(FolderSyncApp, self).__init__(*args, **kw)

        self.panel = wx.Panel(self)
        self.create_widgets()

    def create_widgets(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Textbox for delete_folder
        delete_folder_label = wx.StaticText(self.panel, label="Folder to Delete:")
        self.delete_folder_text = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        sizer.Add(delete_folder_label, 0, wx.ALL, 5)
        sizer.Add(self.delete_folder_text, 0, wx.EXPAND|wx.ALL, 5)

        # Textboxes for source_folder and destination_folder
        source_folder_label = wx.StaticText(self.panel, label="Source Folder:")
        self.source_folder_text = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        sizer.Add(source_folder_label, 0, wx.ALL, 5)
        sizer.Add(self.source_folder_text, 0, wx.EXPAND|wx.ALL, 5)

        dest_folder_label = wx.StaticText(self.panel, label="Destination Folder:")
        self.dest_folder_text = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        sizer.Add(dest_folder_label, 0, wx.ALL, 5)
        sizer.Add(self.dest_folder_text, 0, wx.EXPAND|wx.ALL, 5)

        # Buttons for delete_folder and synchronize_folders
        delete_folder_button = wx.Button(self.panel, label="Delete Folder", size=(150, 30))
        delete_folder_button.Bind(wx.EVT_BUTTON, self.on_delete_folder)
        sizer.Add(delete_folder_button, 0, wx.ALL, 5)

        sync_folders_button = wx.Button(self.panel, label="Sync Folders", size=(150, 30))
        sync_folders_button.Bind(wx.EVT_BUTTON, self.on_sync_folders)
        sizer.Add(sync_folders_button, 0, wx.ALL, 5)

        self.panel.SetSizer(sizer)
        self.Show()

    def on_delete_folder(self, event):
        folder_path = self.delete_folder_text.GetValue()
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                wx.MessageBox(f"Successfully deleted the folder: '{folder_path}'.", "Success", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox(f"Error: Folder '{folder_path}' does not exist.", "Error", wx.OK | wx.ICON_ERROR)

    def on_sync_folders(self, event):
        source_folder = self.source_folder_text.GetValue()
        dest_folder = self.dest_folder_text.GetValue()

        if not os.path.exists(source_folder):
            wx.MessageBox(f"Error: Source folder '{source_folder}' does not exist.", "Error", wx.OK | wx.ICON_ERROR)
            return

        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        try:
            self.synchronize_folders(source_folder, dest_folder)
            wx.MessageBox("Synchronization completed successfully.", "Success", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def synchronize_folders(self, source_folder, destination_folder):
        dcmp = filecmp.dircmp(source_folder, destination_folder)

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for file in dcmp.diff_files + dcmp.left_only:
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, file)

            if os.path.isdir(source_path):
                self.synchronize_folders(source_path, destination_path)
            else:
                shutil.copy2(source_path, destination_path)

        for file in dcmp.right_only:
            file_path = os.path.join(destination_folder, file)

            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)

        for subfolder in dcmp.common_dirs:
            self.synchronize_folders(
                os.path.join(source_folder, subfolder),
                os.path.join(destination_folder, subfolder)
            )


if __name__ == '__main__':
    app = wx.App(False)
    frame = FolderSyncApp(None, title="Folder Synchronization Tool", size=(400, 300))
    app.MainLoop()















