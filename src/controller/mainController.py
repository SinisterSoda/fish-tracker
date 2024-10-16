from tkinter import messagebox, filedialog
import tkinter as tk
import json
import os

from view.rootView import rootView
from model.sessionModel import sessionModel
from view.compareView import compareView

class MainController: 
    def __init__(self):
        
        
        self.fish_data = []
        self.water_type = "Unspecified/Mixed"
        self.bait_type = "Unspecified/Mixed"
        
        self.session_data = sessionModel(self.fish_data, self.water_type, self.bait_type)
        self.rootView = rootView(self.session_data)
        self.rootView.bind("add_fish", self.add_fish)
        self.rootView.bind("bait_change", self.on_bait_change)
        self.rootView.bind("water_change", self.on_water_change)
        
        self.rootView.bind_menu("new", self.new_session)
        self.rootView.bind_menu("save", self.save_session)
        self.rootView.bind_menu("load", self.load_session)
        self.rootView.bind_menu("combine", self.combine_sessions)
        self.rootView.bind_menu("compare", self.compare_sessions)
        
        self.rootView.table.bind("<Double-1>", self.edit_fish)
        
    
        self.ensure_sessions_folder()
        self.rootView.mainloop()
        
        
        
    def ensure_sessions_folder(self):
        self.sessions_folder = os.path.join(os.getcwd(), "sessions")
        if not os.path.exists(self.sessions_folder):
            os.makedirs(self.sessions_folder)

    def new_session(self):
        if not self.session_data.is_empty():
            if messagebox.askyesno("Unsaved Data", "You have unsaved data. Do you want to save it?"):
                self.save_session()

        self.session_data.clear()
        self.rootView.update_data(self.session_data)  # Refresh the tree view

    def add_fish(self):#needs fixing
        fish_name = self.fish_name_entry.get().strip()
        try:
            fish_count = int(self.fish_count_entry.get().strip())
            if fish_name and fish_count >= 0:
                self.session_data.add_fish({"name": fish_name, "count": fish_count})
                self.rootView.update_data(self.session_data)
                #self.update_tree(self.session_data)  # Update the tree view
                self.clear_inputs()
            else:
                messagebox.showwarning("Input Error", "Please enter a valid fish name and count.")
        except ValueError:
            messagebox.showwarning("Input Error", "Count must be a valid integer.")
            
    
             
    def save_session(self):
        self.session_data.save_session()
        
    def clear_inputs(self):
        self.rootView.clear_inputs()
        
    def load_session(self):
        self.session_data = sessionModel.load_session()
        self.rootView.update_data(self.session_data)
        
    def on_bait_change(self, *args):
        #print(self.rootView.bait_type_var.get())
        bait = self.rootView.bait_type_var.get()
        self.session_data.bait_type = bait
        
    def on_water_change(self, *args):
        #print(self.rootView.water_type_var.get())
        water = self.rootView.water_type_var.get()
        self.session_data.water_type = water
        
    def combine_sessions(self):
        file_paths = filedialog.askopenfilenames(initialdir=self.sessions_folder, filetypes=[("JSON files", "*.json")])
        if not file_paths:
            return

        combined_fish_data = []
        water_types = set()
        bait_types = set()

        for file_path in file_paths:
            with open(file_path, 'r') as json_file:
                session_data = json.load(json_file)
                water_types.add(session_data.get("water_type", "Fresh Water"))
                bait_types.add(session_data.get("bait_type", "Bait Paste"))
                combined_fish_data.extend(session_data.get("fish_data", []))

        # Determine combined water type
        if len(water_types) == 1:
            combined_water_type = water_types.pop()
        else:
            combined_water_type = "Unspecified/Mixed"

        # Determine combined bait type
        if len(bait_types) == 1:
            combined_bait_type = bait_types.pop()
        else:
            combined_bait_type = "Unspecified/Mixed"

        # Combine fish data
        fish_data = self.aggregate_fish_data(combined_fish_data)
        water_type = combined_water_type
        bait_type = combined_bait_type
        self.session_data = sessionModel(fish_data, water_type, bait_type)
        
        # Update UI
        self.rootView.update_data(self.session_data)
        
    def aggregate_fish_data(self, fish_data):
        fish_count_dict = {}
        for fish in fish_data:
            name = fish['name']
            count = fish['count']
            if name in fish_count_dict:
                fish_count_dict[name] += count
            else:
                fish_count_dict[name] = count
        return [{"name": name, "count": count} for name, count in fish_count_dict.items()]
    
    def edit_fish(self, event):
        selected_item = self.rootView.table.selection()
        if not selected_item:
            return

        item = self.rootView.table.item(selected_item)
        fish_name, fish_count = item['values'][:2]

        # Create edit pop-up
        edit_window = tk.Toplevel(self.rootView.root)
        edit_window.title("Edit Fish")

        # Create UI elements in the order they appear
        tk.Label(edit_window, text="Fish Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        fish_name_entry = tk.Entry(edit_window, width=20)
        fish_name_entry.grid(row=0, column=1, padx=5, pady=5)
        fish_name_entry.insert(0, fish_name)

        tk.Label(edit_window, text="Count").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        fish_count_entry = tk.Entry(edit_window, width=10)
        fish_count_entry.grid(row=1, column=1, padx=5, pady=5)
        fish_count_entry.insert(0, fish_count)

        def save_changes():
            new_fish_name = fish_name_entry.get().strip()
            try:
                new_fish_count = int(fish_count_entry.get().strip())
                if new_fish_name and new_fish_count >= 0:
                    index = self.rootView.table.index(selected_item)
                    #self.fish_data[index] = {"name": new_fish_name, "count": new_fish_count}
                    self.session_data.update_at(index, {"name": new_fish_name, "count": new_fish_count})
                    self.rootView.update_data(self.session_data)
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Input Error", "Please enter a valid fish name and count.")
            except ValueError:
                messagebox.showwarning("Input Error", "Count must be a valid integer.")

        save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        
    def compare_sessions(self):
        file_paths = filedialog.askopenfilenames(initialdir=self.sessions_folder, title="Select up to 3 JSON files",
                                                   filetypes=[("JSON files", "*.json")])
        if not file_paths or len(file_paths) > 3:
            messagebox.showwarning("Selection Error", "Please select up to 3 files.")
            return

        self.compare_table = compareView(self.rootView.root, file_paths)

    
            