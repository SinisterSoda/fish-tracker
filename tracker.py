import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json
import os

class FishTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fish Tracker")

        self.fish_data = []
        self.water_type = "Unspecified/Mixed"
        self.bait_type = "Unspecified/Mixed"
        self.sort_order = {"Fish": True, "Count": True, "Percentage": True}

        # Create UI components
        self.create_widgets()
        self.create_menu()
        self.ensure_sessions_folder()

    def create_widgets(self):
        # Frame for input
        input_frame = tk.Frame(self.root)
        input_frame.grid(pady=10)

        # Water Type Dropdown
        tk.Label(input_frame, text="Water Type").grid(row=0, column=0, sticky="w", padx=(5, 0))
        self.water_type_var = tk.StringVar(value=self.water_type)
        self.water_type_dropdown = ttk.Combobox(input_frame, textvariable=self.water_type_var, 
                                                  values=["Unspecified/Mixed", "Fresh Water", "Salt Water"])
        self.water_type_dropdown.grid(row=1, column=0, sticky="w", padx=(5, 0), pady=(5, 0))

        # Bait Type Dropdown
        tk.Label(input_frame, text="Bait Type").grid(row=0, column=1, sticky="w", padx=(5, 0))
        self.bait_type_var = tk.StringVar(value=self.bait_type)
        self.bait_type_dropdown = ttk.Combobox(input_frame, textvariable=self.bait_type_var, 
                                                values=["Unspecified/Mixed", "Bait Paste", "Worm", "Shrimp", "Fish Fillet"])
        self.bait_type_dropdown.grid(row=1, column=1, sticky="w", padx=(5, 0), pady=(5, 0))

        # Fish Name Entry
        tk.Label(input_frame, text="Fish Name").grid(row=3, column=0, sticky="w", padx=(5, 0))
        self.fish_name_entry = tk.Entry(input_frame, width=20)
        self.fish_name_entry.grid(row=4, column=0, sticky="w", padx=(5, 0))

        # Fish Count Entry
        tk.Label(input_frame, text="Count").grid(row=3, column=1, sticky="w", padx=(5, 0), pady=(5, 0))
        self.fish_count_entry = tk.Entry(input_frame, width=10)
        self.fish_count_entry.grid(row=4, column=1, sticky="w", padx=(5, 0), pady=(5, 0))

        # Add Fish Button
        add_button = tk.Button(input_frame, text="Add Fish", command=self.add_fish)
        add_button.grid(row=5, column=0, columnspan=2, sticky="w", padx=(5, 0), pady=(5, 0))

        # Separator between inputs and table
        separator = ttk.Separator(self.root, orient="horizontal")
        separator.grid(row=6, column=0, columnspan=2, pady=(10, 5), sticky="ew")

        # Label for editing instructions
        edit_label = tk.Label(self.root, text="Double-click a fish entry to edit.")
        edit_label.grid(row=7, pady=(10, 0))

        # Treeview for displaying fish data with percentages
        self.tree = ttk.Treeview(self.root, columns=("Fish", "Count", "Percentage"), show="headings")
        self.tree.heading("Fish", text="Fish", command=lambda: self.sort_column("Fish"))
        self.tree.heading("Count", text="Count", command=lambda: self.sort_column("Count"))
        self.tree.heading("Percentage", text="Percentage", command=lambda: self.sort_column("Percentage"))
        self.tree.grid(row=9, pady=(10, 30), padx=(10, 10))

        # Bind double-click event to edit fish
        self.tree.bind("<Double-1>", self.edit_fish)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Session", command=self.new_session)
        file_menu.add_command(label="Save Session", command=self.save_session)
        file_menu.add_command(label="Load Session", command=self.load_session)
        file_menu.add_command(label="Combine Sessions", command=self.combine_sessions)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)

        # Compare menu
        compare_menu = tk.Menu(menu_bar, tearoff=0)
        compare_menu.add_command(label="Compare Sessions", command=self.compare_sessions)
        menu_bar.add_cascade(label="Compare", menu=compare_menu)

        self.root.config(menu=menu_bar)

    def ensure_sessions_folder(self):
        self.sessions_folder = os.path.join(os.getcwd(), "sessions")
        if not os.path.exists(self.sessions_folder):
            os.makedirs(self.sessions_folder)

    def new_session(self):
        if self.fish_data:
            if messagebox.askyesno("Unsaved Data", "You have unsaved data. Do you want to save it?"):
                self.save_session()

        self.fish_data.clear()  # Clear the data
        self.water_type = "Unspecified/Mixed"
        self.bait_type = "Unspecified/Mixed"
        self.update_tree()  # Refresh the tree view

    def add_fish(self):
        fish_name = self.fish_name_entry.get().strip()
        try:
            fish_count = int(self.fish_count_entry.get().strip())
            if fish_name and fish_count >= 0:
                self.fish_data.append({"name": fish_name, "count": fish_count})
                self.update_tree()  # Update the tree view
                self.clear_inputs()
            else:
                messagebox.showwarning("Input Error", "Please enter a valid fish name and count.")
        except ValueError:
            messagebox.showwarning("Input Error", "Count must be a valid integer.")

    def clear_inputs(self):
        self.fish_name_entry.delete(0, tk.END)
        self.fish_count_entry.delete(0, tk.END)
        self.water_type_var.set(self.water_type)
        self.bait_type_var.set(self.bait_type)
        self.fish_name_entry.focus()

    def edit_fish(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item)
        fish_name, fish_count = item['values'][:2]

        # Create edit pop-up
        edit_window = tk.Toplevel(self.root)
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
                    index = self.tree.index(selected_item)
                    self.fish_data[index] = {"name": new_fish_name, "count": new_fish_count}
                    self.update_tree()  # Update the tree view
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Input Error", "Please enter a valid fish name and count.")
            except ValueError:
                messagebox.showwarning("Input Error", "Count must be a valid integer.")

        save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def update_tree(self):
        # Clear the tree
        self.tree.delete(*self.tree.get_children())

        if not self.fish_data:
            self.tree.insert("", "end", values=("Total", 0, "-----"))
            return

        total_count = sum(item['count'] for item in self.fish_data)
        for fish in self.fish_data:
            percentage = (fish['count'] / total_count) * 100 if total_count > 0 else 0
            self.tree.insert("", "end", values=(fish['name'], fish['count'], f"{percentage:.2f}%"))

        # Add Total row at the bottom
        self.tree.insert("", "end", values=("Total", total_count, "-----"))

    def save_session(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", initialdir=self.sessions_folder, 
                                                   filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        session_data = {
            "water_type": self.water_type_var.get(),
            "bait_type": self.bait_type_var.get(),
            "fish_data": self.fish_data
        }
        
        with open(file_path, 'w') as f:
            json.dump(session_data, f, indent=4)

    def load_session(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", initialdir=self.sessions_folder, 
                                                filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        with open(file_path, 'r') as f:
            session_data = json.load(f)

        self.water_type_var.set(session_data.get("water_type", "Unspecified/Mixed"))
        self.bait_type_var.set(session_data.get("bait_type", "Unspecified/Mixed"))
        self.fish_data = session_data.get("fish_data", [])
        self.update_tree()  # Update the tree view

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
        self.fish_data = self.aggregate_fish_data(combined_fish_data)
        self.water_type = combined_water_type
        self.bait_type = combined_bait_type
        
        # Update UI
        self.water_type_var.set(self.water_type)
        self.bait_type_var.set(self.bait_type)
        self.update_tree()

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

    def compare_sessions(self):
        file_paths = filedialog.askopenfilenames(initialdir=self.sessions_folder, title="Select up to 3 JSON files",
                                                   filetypes=[("JSON files", "*.json")])
        if not file_paths or len(file_paths) > 3:
            messagebox.showwarning("Selection Error", "Please select up to 3 files.")
            return

        compare_window = tk.Toplevel(self.root)
        compare_window.title("Compare Sessions")
        
        self.compare_sort_orders = []

        for index, file_path in enumerate(file_paths):
            with open(file_path, 'r') as json_file:
                session_data = json.load(json_file)
                self.compare_sort_orders.append(None)
                self.create_compare_table(compare_window, session_data, file_path, index)

    def create_compare_table(self, parent, session_data, file_path, index):
        frame = tk.Frame(parent)
        frame.grid(row=0, column=index, padx=10, pady=10)
        
        print(index);
        self.compare_sort_orders[index] = {"Fish": True, "Count": True, "Percentage": True}

        # Extracting the session name from the file path
        session_name = os.path.basename(file_path).replace(".json", "")
        label = tk.Label(frame, text=session_name)
        label.pack()

        tree = ttk.Treeview(frame, columns=("Fish", "Count", "Percentage"), show="headings")

        # Define a command for sorting
        def sort_column_compare(col):
            self.sort_compare_tree(session_data.get("fish_data", []), tree, col, index)

        # Configure headings with sorting functionality
        tree.heading("Fish", text="Fish", command=lambda: sort_column_compare("Fish"))
        tree.heading("Count", text="Count", command=lambda: sort_column_compare("Count"))
        tree.heading("Percentage", text="Percentage", command=lambda: sort_column_compare("Percentage"))
        tree.pack()

        # Initially populate the tree
        self.populate_compare_tree(tree, session_data)

    def populate_compare_tree(self, tree, session_data):
        fish_data = session_data.get("fish_data", [])
        total_count = sum(item['count'] for item in fish_data)
        for fish in fish_data:
            percentage = (fish['count'] / total_count) * 100 if total_count > 0 else 0
            tree.insert("", "end", values=(fish['name'], fish['count'], f"{percentage:.2f}%"))

        # Add Total row at the bottom
        tree.insert("", "end", values=("Total", total_count, "-----"))

    def sort_compare_tree(self, fish_data, tree, key, index):
        total_count = sum(item['count'] for item in fish_data)
        self.compare_sort_orders[index][key] = not self.compare_sort_orders[index][key]
        ascending = self.compare_sort_orders[index][key]
        if key == "Fish":
            fish_data.sort(key=lambda x: x['name'], reverse=not ascending)  # Sort by Fish name
        elif key == "Count":
            fish_data.sort(key=lambda x: x['count'], reverse=not ascending)  # Sort by Count
        elif key == "Percentage":
            
            for fish in fish_data:
                fish['percentage'] = (fish['count'] / total_count) * 100 if total_count > 0 else 0
            fish_data.sort(key=lambda x: x['percentage'], reverse=not ascending)  # Sort by Percentage

        # Clear the tree and reinsert sorted data
        tree.delete(*tree.get_children())
        self.populate_compare_tree(tree, {"fish_data": fish_data})  # Repopulate with sorted data

    #tree.insert("", "end", values=("Total", total_count, "-----"))

    def sort_column(self, col):
        if col in self.sort_order:
            self.sort_order[col] = not self.sort_order[col]
            ascending = self.sort_order[col]
            self.fish_data.sort(key=lambda x: (x[col.lower()] if col != "Percentage" else x['count']/sum(item['count'] for item in self.fish_data)), 
                                reverse=not ascending)
            self.update_tree()  # Refresh the tree view with sorted data

if __name__ == "__main__":
    root = tk.Tk()
    app = FishTrackerApp(root)
    root.mainloop()
