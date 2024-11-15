import tkinter as tk
from tkinter import ttk

class ExportView:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Export CSV")
        self.window.geometry("400x300")
        
        self._on_export = None
        self._on_close = None
        
        self.default_names = {
            'name': 'name',
            'count': 'count',
            'missed': 'missed'
        }
        
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def create_widgets(self):
        # Instructions label
        tk.Label(self.window, 
                text="Customize CSV column names:",
                wraplength=350).pack(pady=10)
        
        # Create mapping frame
        mapping_frame = ttk.Frame(self.window)
        mapping_frame.pack(pady=10, padx=20, fill='x')
        
        # Create entry for each field
        self.column_vars = {}
        
        for field, default in self.default_names.items():
            # Container frame for each mapping
            field_frame = ttk.Frame(mapping_frame)
            field_frame.pack(fill='x', pady=5)
            
            # Label for the field
            ttk.Label(field_frame, 
                     text=f"{field.capitalize()} column:").pack(side='left', padx=5)
            
            # Entry for column name
            var = tk.StringVar(value=default)
            self.column_vars[field] = var
            
            entry = ttk.Entry(field_frame, 
                            textvariable=var,
                            width=30)
            entry.pack(side='right', padx=5)
        
        # Buttons frame
        button_frame = ttk.Frame(self.window)
        button_frame.pack(side='bottom', pady=20)
        
        ttk.Button(button_frame, 
                  text="Export", 
                  command=self.on_export).pack(side='left', padx=10)
        
        ttk.Button(button_frame, 
                  text="Cancel", 
                  command=self.on_close).pack(side='left', padx=10)
        
    def get_column_names(self):
        return {field: var.get().strip() for field, var in self.column_vars.items()}
    
    def bind(self, event, callback):
        if event == "export":
            self._on_export = callback
        elif event == "close":
            self._on_close = callback
            
    def on_export(self):
        if self._on_export:
            self._on_export()
            
    def on_close(self):
        if self._on_close:
            self._on_close()
        self.destroy()
        
    def destroy(self):
        if self.window:
            self.window.destroy()
            self.window = None 