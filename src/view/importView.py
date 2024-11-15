import tkinter as tk
from tkinter import ttk

class ImportView:
    def __init__(self, root, csv_headers):
        self.window = tk.Toplevel(root)
        self.window.title("Import CSV")
        self.window.geometry("400x300")
        
        self._on_import = None
        self._on_close = None
        
        self.csv_headers = csv_headers
        self.required_fields = ['name', 'count', 'missed']
        
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def create_widgets(self):
        # Instructions label
        tk.Label(self.window, 
                text="Map CSV columns to required fields:",
                wraplength=350).pack(pady=10)
        
        # Create mapping frame
        mapping_frame = ttk.Frame(self.window)
        mapping_frame.pack(pady=10, padx=20, fill='x')
        
        # Create dropdown for each required field
        self.mapping_vars = {}
        
        for i, field in enumerate(self.required_fields):
            # Container frame for each mapping
            field_frame = ttk.Frame(mapping_frame)
            field_frame.pack(fill='x', pady=5)
            
            # Label for the field
            ttk.Label(field_frame, 
                     text=f"{field.capitalize()}:").pack(side='left', padx=5)
            
            # Dropdown for column selection
            var = tk.StringVar()
            self.mapping_vars[field] = var
            
            dropdown = ttk.Combobox(field_frame, 
                                  textvariable=var,
                                  values=[''] + self.csv_headers,
                                  state='readonly',
                                  width=30)
            dropdown.pack(side='right', padx=5)
            
            # Try to auto-match columns
            for header in self.csv_headers:
                if header.lower() == field.lower():
                    var.set(header)
                    break
        
        # Buttons frame
        button_frame = ttk.Frame(self.window)
        button_frame.pack(side='bottom', pady=20)
        
        ttk.Button(button_frame, 
                  text="Import", 
                  command=self.on_import).pack(side='left', padx=10)
        
        ttk.Button(button_frame, 
                  text="Cancel", 
                  command=self.on_close).pack(side='left', padx=10)
        
    def get_mapping(self):
        return {field: var.get() for field, var in self.mapping_vars.items()}
    
    def bind(self, event, callback):
        if event == "import":
            self._on_import = callback
        elif event == "close":
            self._on_close = callback
            
    def on_import(self):
        if self._on_import:
            self._on_import()
            
    def on_close(self):
        if self._on_close:
            self._on_close()
        self.destroy()
        
    def destroy(self):
        if self.window:
            self.window.destroy()
            self.window = None 