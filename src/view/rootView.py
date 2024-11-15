import tkinter as tk
from tkinter import ttk
from view.menuView import menuView
from view.tableView import tableView
from model.sessionModel import sessionModel

class rootView:
    def __init__(self, session_data: sessionModel):
        self.root = tk.Tk()
        self.root.title("Fish Tracker")
        
        self.water_type = session_data.water_type
        self.bait_type = session_data.bait_type
        self.fish_data = session_data.fish_data
        self.water_types = ["Unspecified/Mixed", "Fresh Water", "Salt Water"]
        self.bait_types = ["Unspecified/Mixed", "Bait Paste", "Worm", "Shrimp", "Fish Fillet"]
        
        self._add_fish = None
        self._on_bait_change = None
        self._on_water_change = None
        
        self._on_destroyed = None
        
        self.root.bind("<Destroy>", self.on_self_destroy)
        
        self.create_widgets()
        self.create_menu()
    
    def mainloop(self):
        self.root.mainloop()
        
        
    def create_widgets(self):
        # Frame for input
        input_frame = tk.Frame(self.root)
        input_frame.grid(pady=10)

        # Water Type Dropdown
        tk.Label(input_frame, text="Water Type").grid(row=0, column=0, sticky="w", padx=(5, 0))
        self.water_type_var = tk.StringVar(value=self.water_type)
        self.water_type_dropdown = ttk.Combobox(input_frame, textvariable=self.water_type_var,values=self.water_types)
        self.water_type_dropdown.grid(row=1, column=0, sticky="w", padx=(5, 0), pady=(5, 0))

        # Bait Type Dropdown
        tk.Label(input_frame, text="Bait Type").grid(row=0, column=1, sticky="w", padx=(5, 0))
        self.bait_type_var = tk.StringVar(value=self.bait_type)
        self.bait_type_dropdown = ttk.Combobox(input_frame, textvariable=self.bait_type_var,values=self.bait_types)
        self.bait_type_dropdown.grid(row=1, column=1, sticky="w", padx=(5, 0), pady=(5, 0))
        
        self.water_type_var.trace_add('write', self.on_water_change)  # When var1 changes, call on_var_change
        self.bait_type_var.trace_add('write', self.on_bait_change)

        # Fish Name Entry
        tk.Label(input_frame, text="Fish Name").grid(row=3, column=0, sticky="w", padx=(5, 0))
        self.fish_name_entry = tk.Entry(input_frame, width=20)
        self.fish_name_entry.grid(row=4, column=0, sticky="w", padx=(5, 0))

        # Fish Count Entry
        tk.Label(input_frame, text="Count").grid(row=3, column=1, padx=(5, 0), pady=(5, 0))
        self.fish_count_entry = tk.Entry(input_frame, width=5)
        self.fish_count_entry.insert(0, "0")
        self.fish_count_entry.grid(row=4, column=1, padx=(5, 0), pady=(5, 0))
        
        # Missed Count Entry
        tk.Label(input_frame, text="Missed").grid(row=3, column=2, padx=(5, 0), pady=(5, 0))
        self.missed_count_entry = tk.Entry(input_frame, width=5)
        self.missed_count_entry.insert(0, "0")
        self.missed_count_entry.grid(row=4, column=2, padx=(5, 0), pady=(5, 0))

        # Add Fish Button
        add_button = tk.Button(input_frame, text="Add Fish", command=self.add_fish)
        add_button.grid(row=5, column=0, columnspan=2, sticky="w", padx=(5, 0), pady=(5, 0))

        # Separator between inputs and table
        separator = ttk.Separator(self.root, orient="horizontal")
        separator.grid(row=6, column=0, columnspan=2, pady=(10, 5), sticky="ew")

        # Label for editing instructions
        edit_label = tk.Label(self.root, text="Double-click a fish entry to edit.")
        edit_label.grid(row=7, pady=(10, 0))
        
        self.table = tableView(self.root, self.fish_data)
    
    def on_bait_change(self, *args):
        if self._on_bait_change is not None and callable(self._on_bait_change):
            self._on_bait_change(*args)
     
    def on_water_change(self, *args):
        if self._on_water_change is not None and callable(self._on_water_change):
            self._on_water_change(*args)   
    
        
    def create_menu(self):
        self.menu_bar = menuView(self.root)
        
    def bind_menu(self, cmd, f):
        self.menu_bar.bind(cmd, f)
    
    def bind(self, cmd, fn):
        if cmd == "add_fish":
            self._add_fish = fn
        elif cmd == "bait_change":
            self._on_bait_change = fn
        elif cmd == "water_change":
            self._on_water_change = fn
        elif cmd == "<Destroy>":
            self._on_destroyed = fn

        
        
        
    def update_data(self, session_data):
        self.water_type = session_data.water_type
        self.bait_type = session_data.bait_type
        self.fish_data = session_data.fish_data
        self.water_type_var.set(self.water_type)
        self.bait_type_var.set(self.bait_type)
        
        self.update_table()
        
        
    def update_table(self):
        self.table.update_tree(self.fish_data)
        
    def clear_inputs(self):
        self.fish_name_entry.delete(0, tk.END)
        self.fish_count_entry.delete(0, tk.END)
        self.missed_count_entry.delete(0, tk.END)  # Clear missed entry
        self.water_type_var.set(self.water_type)
        self.bait_type_var.set(self.bait_type)
        self.fish_name_entry.focus()
        
    def get_fish_name(self):
        return self.fish_name_entry.get()
    def get_fish_count(self):
        return self.fish_count_entry.get()
    def get_missed_count(self):
        return self.missed_count_entry.get()  # New method for missed count
    def get_water_type(self):
        return self.water_type_var.get()
    def get_bait_type(self):
        return self.bait_type_var.get()
    
    def add_fish(self):
        if self._add_fish is not None and callable(self._add_fish):
            self._add_fish()
            
    def quit(self):
        self.root.quit()
            
    def on_self_destroy(self, *args):
        #do my own stuff

        
        if self._on_destroyed is not None and callable(self._on_destroyed):
            self._on_destroyed(*args)
        
        
        
    
        

