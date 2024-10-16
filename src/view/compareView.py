import json
import os
import tkinter as tk

from view.tableView import tableView
from model.sessionModel import sessionModel

class compareView:
    def __init__(self, root, file_paths):
        self.root = root
        self.compare_window = tk.Toplevel(self.root)
        self.compare_window.title("Compare Sessions")

        for index, file_path in enumerate(file_paths):
            session_data = sessionModel.load_file(file_path)
            self.create_compare_table(session_data, file_path, index)
    
    
    def create_compare_table(self, session_data: sessionModel, file_path, index):
        frame = tk.Frame(self.compare_window)
        frame.grid(row=0, column=index, padx=10, pady=10)
        
        
        
        # Extracting the session name from the file path
        session_name = os.path.basename(file_path).replace(".json", "")
        label = tk.Label(frame, text=session_name)
        label.grid(row=0, column=0)
        

        self.table = tableView(frame, session_data.fish_data)

        

