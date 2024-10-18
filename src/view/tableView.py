import tkinter as tk
from tkinter import ttk
from model.sessionModel import sessionModel

class tableView:
    def __init__(self, root, data):
        self.data = data
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=9, pady=(10, 30), padx=(10, 10))
        
        # Checkbox for hiding rows with 0 catches
        self.hide_zero_catches_var = tk.BooleanVar(value=False)
        self.hide_zero_catches_checkbox = tk.Checkbutton(
            self.frame,
            text="Hide rows with 0 seen",
            variable=self.hide_zero_catches_var,
            command=self.update_tree
        )
        self.hide_zero_catches_checkbox.grid(row=0, column=0, sticky="w")
        
        heading = ("Name", "Count", "Percentage", "Missed",  "Number Seen", "Catch Percentage", "Seen Percentage")
        
        # Treeview for displaying fish data with percentages
        self.tree = ttk.Treeview(self.frame, columns=heading, show="headings")
        self.tree.heading("Name", text="Fish", command=lambda: self.sort_column("Name"))
        self.tree.heading("Count", text="Caught", command=lambda: self.sort_column("Count"))
        self.tree.heading("Missed", text="Missed", command=lambda: self.sort_column("Missed"))
        self.tree.heading("Percentage", text="Percentage", command=lambda: self.sort_column("Percentage"))
        self.tree.heading("Number Seen", text="Seen", command=lambda: self.sort_column("Number Seen"))
        self.tree.heading("Catch Percentage", text="Catch Rate", command=lambda: self.sort_column("Catch Percentage"))
        self.tree.heading("Seen Percentage", text="See Rate", command=lambda: self.sort_column("Seen Percentage"))
        self.tree.grid(row=1, pady=(10, 30), padx=(10, 10))
        
        self.tree.column("Name", width=100, anchor="center")  # Adjust width as needed
        self.tree.column("Count", width=65, anchor="center")
        self.tree.column("Missed", width=65, anchor="center")
        self.tree.column("Percentage", width=90, anchor="center")
        self.tree.column("Number Seen", width=65, anchor="center")
        self.tree.column("Catch Percentage", width=90, anchor="center")
        self.tree.column("Seen Percentage", width=65, anchor="center")
        
        
        self.sort_order = {
            "Name": True,
            "Missed": True,
            "Count": True,
            "Percentage": True,
            "Number Seen": True,
            "Catch Percentage": True,
            "Seen Percentage": True
        }
        
        self.update_tree()
        
    def bind(self, cmd, fn):
        # Bind bind event to value
        self.tree.bind(cmd, fn)#"<Double-1>"
        
    def update_tree(self, new_data=None):
        if new_data is not None:
            self.data = new_data
        # Clear the tree
        self.tree.delete(*self.tree.get_children())
        blank_sep = "------"
        if not self.data:
            self.tree.insert("", "end", values=(
                "Total",
                0,
                blank_sep,
                0,
                0,
                blank_sep,
                blank_sep
            ))
            return

        total_count = sessionModel.calculate_total_caught_from(self.data)
        missed_count = sessionModel.calculate_total_missed_from(self.data)
        total_seen = sessionModel.calculate_total_seen_from(self.data)
        for fish in self.data:
            if self.hide_zero_catches_var.get() and fish['count'] == 0 and fish.get('missed', 0) == 0:
                continue  # Skip rows with 0 catches if the checkbox is checked
            
            percentage = (fish['count'] / total_count) * 100 if total_count > 0 else 0
            number_seen = fish['count'] + fish.get('missed', 0)  # Calculate Number Seen
            catch_percentage = (fish["count"] / number_seen * 100) if number_seen > 0 else 0
            seen_percentage = (number_seen / total_seen * 100) if total_seen > 0 else 0
            
            
            #heading = ("Name", "Count", "Percentage", "Missed",  "Number Seen", "Catch Percentage", "Seen Percentage")
            self.tree.insert("", "end", values=(
                fish['name'], 
                fish['count'],
                f"{percentage:.2f}%",
                fish["missed"], 
                number_seen,
                f"{catch_percentage:.2f}%",
                f"{seen_percentage:.2f}%"
            ))

        # Add Total row at the bottom
        # Calculate the total catch percentage
        total_catch_percentage = (total_count / total_seen * 100) if total_seen > 0 else 0
        
        self.tree.insert("", "end", values=(
            "Total",
            total_count,
            blank_sep,
            missed_count,
            total_count + missed_count,
            f"{total_catch_percentage:.2f}%",
            blank_sep
        ))
        
    def sort_key(self, fish, col, total_count, total_seen):
        if col == "Percentage":
            return fish['count'] / total_count if total_count > 0 else 0
        elif col == "Number Seen":
            return fish['count'] + fish.get('missed', 0)
        elif col == "Catch Percentage":
            count = fish['count']
            missed = fish.get('missed', 0)
            number_seen = count + missed
            return (count / number_seen * 100) if number_seen > 0 else 0
        elif col == "Seen Percentage":
            count = fish['count']
            missed = fish.get('missed', 0)
            number_seen = count + missed
            return (number_seen / total_seen * 100) if total_seen > 0 else 0
        else:
            return fish[col.lower()]  # Assuming other columns use the key directly
    
    def sort_column(self, col):
        total_count = sessionModel.calculate_total_caught_from(self.data)
        total_seen = sessionModel.calculate_total_seen_from(self.data)
        if col in self.sort_order:
            k = col.lower()
            
            self.sort_order[col] = not self.sort_order[col]
            ascending = self.sort_order[col]

            self.data.sort(key=lambda x: self.sort_key(x, col, total_count, total_seen), reverse=not ascending)
            self.update_tree(self.data)  # Refresh the tree view with sorted data
            
            
    def selection(self):
        return self.tree.selection()
    
    def item(self, index):
        return self.tree.item(index)
    
    def index(self, value):
        return self.tree.index(value)