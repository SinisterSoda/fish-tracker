from tkinter import messagebox, filedialog
import tkinter as tk
import json
import os

from functools import partial
import time

from view.rootView import rootView
from model.sessionModel import sessionModel
from view.compareView import compareView
from view.graphView import GraphView
from view.editView import EditView
from view.importView import ImportView
from view.exportView import ExportView

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
        self.rootView.bind_menu("graph", self.graph_current_session)
        self.rootView.bind_menu("graph_other", self.graph_other_session)
        self.rootView.bind_menu("export", self.export_session)
        self.rootView.bind_menu("import", self.import_session)
        
        #self.rootView.table.bind("<Double-1>", self.edit_fish)
        self.last_click_time = 0
        self.is_double_click = False
        self.rootView.table.bind("<ButtonRelease-1>", self.on_click)

        self.edit_window = None
        
        self.graphView = None
        self.otherGraphViews = []  # New list for additional graph windows
        
        self.rootView.bind("<Destroy>", self.kill)
        
        self.import_window = None
        self.export_window = None
        
        self.ensure_sessions_folder()
        self.rootView.mainloop()
        
    def kill(self, *args):
        self.kill_children(args)
        if self.rootView:
            self.rootView.quit()
            self.rootView = None
        
    def kill_children(self, event=None):
        if self.graphView is not None:
            self.graphView.destroy()
            self.graphView = None
        if self.edit_window is not None:  # Destroy edit window if open
            self.edit_window.destroy()
            self.edit_window = None
        # Clean up other graph views
        for graph in self.otherGraphViews:
            if graph is not None:
                graph.destroy()
        self.otherGraphViews.clear()     
        
        
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
        self.focus_root()

    def on_click(self, event):
        current_time = time.time()
        if current_time - self.last_click_time < 0.4:  # 400 ms threshold for double-click
            if not self.is_double_click:
                self.is_double_click = True
                self.rootView.root.after(10, self.perform_edit, event)
        else:
            self.is_double_click = False
        self.last_click_time = current_time

    def perform_edit(self, event):
        self.edit_fish(event)
        self.is_double_click = False

    def add_fish(self):
        fish_name = self.rootView.get_fish_name().strip()
        index_check = self.session_data.fish_index(fish_name)
        if index_check >= 0:
            messagebox.showwarning("Invalid Name", "You cannot reuse a name that already exists")
            return
        try:
            fish_count = int(self.rootView.get_fish_count().strip())
            missed_count = int(self.rootView.get_missed_count().strip())  # Get missed count
            if fish_name and fish_count >= 0 and fish_count >= 0:
                self.session_data.add_fish({
                    "name": fish_name,
                    "count": fish_count,
                    "missed": missed_count
                })
                self.rootView.update_data(self.session_data)
                #self.update_tree(self.session_data)  # Update the tree view
                self.clear_inputs()
            else:
                messagebox.showwarning("Input Error", "Please enter a valid fish name and count.")
        except ValueError:
            messagebox.showwarning("Input Error", "Count and missed must be a valid integer.")
            
    
    def focus_root(self):
        self.rootView.root.focus_force()
             
    def save_session(self):
        self.session_data.save_session()
        self.focus_root()
        
    def clear_inputs(self):
        self.rootView.clear_inputs()
        
    def load_session(self):
        self.session_data = sessionModel.load_session()
        if self.session_data is not None:
            self.rootView.update_data(self.session_data)
        self.focus_root()
        
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
        self.focus_root()
        
    def aggregate_fish_data(self, fish_data):
        fish_count_dict = {}
        for fish in fish_data:
            name = fish['name']
            count = fish['count']
            missed = fish.get('missed', 0)
            if name in fish_count_dict:
                fish_count_dict[name]['count'] += count
                fish_count_dict[name]['missed'] += missed  # Aggregate missed counts
            else:
                fish_count_dict[name] = {'name': name, 'count': count, 'missed': missed}
        return [{'name': fish['name'], 'count': fish['count'], 'missed': fish['missed']} for fish in fish_count_dict.values()]
    

    def save_edit_changes(self):
        if not self.edit_window:
            return

        fish_name = self.edit_window.original_fish_data['name']
        values = self.edit_window.get_values()
        new_fish_name = values['name']
        index_check = self.session_data.fish_index(new_fish_name)
        if index_check >= 0 and fish_name != new_fish_name:
            messagebox.showwarning("Invalid Name", "You cannot reuse a name that already exists")
            return
        try:
            new_fish_count = int(values['count'])
            new_missed_count = int(values['missed'])
            if new_fish_name and new_fish_count >= 0 and new_missed_count >= 0:
                index = self.session_data.fish_index(fish_name)
                self.session_data.update_at(index, {
                    "name": new_fish_name, 
                    "count": new_fish_count,
                    "missed": new_missed_count
                })
                self.rootView.update_data(self.session_data)
                self.edit_window.destroy()
                self.edit_window = None
            else:
                messagebox.showwarning("Input Error", "Please enter a valid fish name and count.")
        except ValueError:
            messagebox.showwarning("Input Error", "Count and missed must be a valid integer.")
        self.focus_root()
            
    def delete_edit_fish(self):
        if not self.edit_window:
            return
        
        fish_name = self.edit_window.original_fish_data['name']
        if messagebox.askyesno("Delete Fish", f"Are you sure you want to delete '{fish_name}'?"):
            index = self.session_data.fish_index(fish_name)
            if index >= 0:
                self.session_data.delete_at(index)
                self.rootView.update_data(self.session_data)
                self.edit_window.destroy()
                self.edit_window = None
        self.focus_root()

    def on_edit_close(self):
        if not self.edit_window:
            return
        self.edit_window = None
        self.focus_root()

    def edit_fish(self, event):
        selected_item = self.rootView.table.selection()
        if not selected_item:
            return
        
        if self.edit_window is not None:
            messagebox.showwarning("Already Editing", "You are already editing a fish.")
            self.edit_window.window.focus_force()
            return
        
        # Check if this is the last selection in the table
        if selected_item[0] == self.rootView.table.tree.get_children()[-1]:
            return

        item = self.rootView.table.item(selected_item)
        fish_name, fish_count, _, missed_count = item['values'][:4]

        # Get the current mouse position
        mouse_x = self.rootView.root.winfo_pointerx()
        mouse_y = self.rootView.root.winfo_pointery()

        fish_data = {
            'name': fish_name,
            'count': fish_count,
            'missed': missed_count
        }

        # Create edit pop-up
        from view.editView import EditView
        self.edit_window = EditView(self.rootView.root, fish_data, mouse_x, mouse_y)
        
        

        self.edit_window.bind("save", self.save_edit_changes)
        self.edit_window.bind("delete", self.delete_edit_fish)
        self.edit_window.bind("close", self.on_edit_close)
        
        
    def compare_sessions(self):
        file_paths = filedialog.askopenfilenames(initialdir=self.sessions_folder, title="Select up to 3 JSON files",
                                                   filetypes=[("JSON files", "*.json")])
        if not file_paths or len(file_paths) > 3:
            messagebox.showwarning("Selection Error", "Please select up to 3 files.")
            return

        self.compare_table = compareView(self.rootView.root, file_paths)

    def graph_current_session(self):
        if self.session_data.is_empty():
            messagebox.showwarning("Empty Session", "There is no data to graph.")
            return

        graph_data = []
        for fish in self.session_data.fish_data:
            total_count = self.session_data.calculate_total_caught()
            total_seen = self.session_data.calculate_total_seen()
            number_seen = fish['count'] + fish.get('missed', 0)
            graph_data.append({
                'name': fish['name'],
                'count': fish['count'],
                'missed': fish.get('missed', 0),
                'percentage': f"{(fish['count'] / total_count * 100):.2f}%" if total_count > 0 else "0.00%",
                'number_seen': number_seen,
                'catch_percentage': f"{(fish['count'] / number_seen * 100):.2f}%" if number_seen > 0 else "0.00%",
                'seen_percentage': f"{(number_seen / total_seen * 100):.2f}%" if total_seen > 0 else "0.00%"
            })
        if self.graphView is not None:
            self.graphView.destroy()
        self.graphView = GraphView(self.rootView.root, graph_data)

    def graph_other_session(self):
        #loaded_session = sessionModel.load_session()
        file_paths = filedialog.askopenfilenames(initialdir=self.sessions_folder, filetypes=[("JSON files", "*.json")])
        if not file_paths:
            return
        
        for file_path in file_paths:
            loaded_session = sessionModel.load_file(file_path)
            if loaded_session:
                graph_data = []
                for fish in loaded_session.fish_data:
                    total_count = loaded_session.calculate_total_caught()
                    total_seen = loaded_session.calculate_total_seen()
                    number_seen = fish['count'] + fish.get('missed', 0)
                    graph_data.append({
                        'name': fish['name'],
                        'count': fish['count'],
                        'missed': fish.get('missed', 0),
                        'percentage': f"{(fish['count'] / total_count * 100):.2f}%" if total_count > 0 else "0.00%",
                        'number_seen': number_seen,
                        'catch_percentage': f"{(fish['count'] / number_seen * 100):.2f}%" if number_seen > 0 else "0.00%",
                        'seen_percentage': f"{(number_seen / total_seen * 100):.2f}%" if total_seen > 0 else "0.00%"
                    })
                new_graph = GraphView(self.rootView.root, graph_data)
                self.otherGraphViews.append(new_graph)
            

    def export_session(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialdir=os.path.join(os.getcwd(), "sessions"),
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return

        self.show_export_window(file_path)
        
    def show_export_window(self, file_path):
        if self.export_window is not None:
            self.export_window.destroy()
        
        self.export_window = ExportView(self.rootView.root)
        self.export_window.bind("export", lambda: self.process_export(file_path))
        self.export_window.bind("close", self.on_export_close)
    
    def process_export(self, file_path):
        if not self.export_window:
            return
            
        column_names = self.export_window.get_column_names()
        
        # Validate column names
        if not all(column_names.values()):
            messagebox.showerror("Error", "All column names must be specified")
            return
            
        try:
            self.session_data.export_to_csv(file_path, column_names)
            self.export_window.destroy()
            self.export_window = None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
        
    def on_export_close(self):
        if self.export_window:
            self.export_window = None
            
    def import_session(self):
        print("import session")
        file_path = filedialog.askopenfilename(
            defaultextension=".csv",
            initialdir=self.sessions_folder,
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return
        
        try:
            headers = sessionModel.get_csv_headers(file_path)
            self.show_import_window(file_path, headers)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV file: {str(e)}")
        
    def show_import_window(self, file_path, headers):
        if self.import_window is not None:
            self.import_window.destroy()
        
        self.import_window = ImportView(self.rootView.root, headers)
        self.import_window.bind("import", lambda: self.process_import(file_path))
        self.import_window.bind("close", self.on_import_close)
    
    def process_import(self, file_path):
        if not self.import_window:
            return
        
        mapping = self.import_window.get_mapping()
        
        # Validate mapping
        if not all(mapping.values()):
            messagebox.showerror("Error", "Please map all required fields")
            return
        
        try:
            fish_data = sessionModel.import_from_csv(file_path, mapping)
            if fish_data:
                self.session_data = sessionModel(fish_data, "Unspecified/Mixed", "Unspecified/Mixed")
                self.rootView.update_data(self.session_data)
                self.import_window.destroy()
                self.import_window = None
            else:
                messagebox.showerror("Error", "CSV file has invalid data, or column mapping is incorrect")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data: {str(e)}")
        
    def on_import_close(self):
        if self.import_window:
            self.import_window = None
        
            