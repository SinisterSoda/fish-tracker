import tkinter as tk
from tkinter import messagebox

class EditView:
    def __init__(self, root, fish_data, mouse_x, mouse_y):
        self.window = tk.Toplevel(root)
        self.window.title("Edit Fish")
        self.window.geometry(f"+{mouse_x}+{mouse_y}")
        
        self._on_save = None
        self._on_delete = None
        self._on_close = None

        self.original_fish_data = fish_data
        
        self.create_widgets(fish_data)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self, fish_data):
        # Fish Name row
        tk.Label(self.window, text="Fish Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.fish_name_entry = tk.Entry(self.window, width=20)
        self.fish_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.fish_name_entry.insert(0, fish_data['name'])

        # Count row with adjustment buttons
        tk.Label(self.window, text="Count").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.fish_count_entry = tk.Entry(self.window, width=10)
        self.fish_count_entry.grid(row=1, column=1, padx=5, pady=5)
        self.fish_count_entry.insert(0, fish_data['count'])

        # Count adjustment buttons - updated styling
        button_font = ('TkDefaultFont', 8)
        button_style = {
            'font': button_font, 
            'width': 1,  # Slightly wider to accommodate padding
            'height': 1,
            'padx': 2,   # Inner horizontal padding
            'pady': 3,   # Inner vertical padding
            'relief': 'raised',
            'borderwidth': 2,
            'border': 2,
            'highlightthickness': 0,
        }
        
        # Count adjustment buttons
        tk.Button(self.window, text="-5", command=lambda: self.adjust_value('count', -5), **button_style).grid(row=1, column=2, padx=2)
        tk.Button(self.window, text="-1", command=lambda: self.adjust_value('count', -1), **button_style).grid(row=1, column=3, padx=2)
        tk.Button(self.window, text="+1", command=lambda: self.adjust_value('count', 1), **button_style).grid(row=1, column=4, padx=2)
        tk.Button(self.window, text="+5", command=lambda: self.adjust_value('count', 5), **button_style).grid(row=1, column=5, padx=2)
        
        # Missed row with adjustment buttons
        tk.Label(self.window, text="Missed").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.missed_count_entry = tk.Entry(self.window, width=10)
        self.missed_count_entry.grid(row=2, column=1, padx=5, pady=5)
        self.missed_count_entry.insert(0, fish_data['missed'])
        
        # Missed adjustment buttons
        tk.Button(self.window, text="-5", command=lambda: self.adjust_value('missed', -5), **button_style).grid(row=2, column=2, padx=2)
        tk.Button(self.window, text="-1", command=lambda: self.adjust_value('missed', -1), **button_style).grid(row=2, column=3, padx=2)
        tk.Button(self.window, text="+1", command=lambda: self.adjust_value('missed', 1), **button_style).grid(row=2, column=4, padx=2)
        tk.Button(self.window, text="+5", command=lambda: self.adjust_value('missed', 5), **button_style).grid(row=2, column=5, padx=2)

        # Action buttons - with similar styling but slightly larger
        action_button_style = {
            'font': ('TkDefaultFont', 12),
            'padx': 10,
            'pady': 5,
            'relief': 'raised',
            'borderwidth': 2,
            'border': 2,
            'highlightthickness': 0,
        }

        save_button = tk.Button(self.window, text="Save Changes", command=self.on_save, **action_button_style)
        save_button.grid(row=3, column=0, columnspan=3, padx=5, pady=10)

        delete_button = tk.Button(self.window, text="Delete", command=self.on_delete, fg="red", **action_button_style)
        delete_button.grid(row=3, column=3, columnspan=3, padx=5, pady=10)

        # Focus the count entry field
        self.fish_count_entry.focus_set()

    def adjust_value(self, field, amount):
        entry = self.fish_count_entry if field == 'count' else self.missed_count_entry
        try:
            current_value = int(entry.get())
            new_value = max(0, current_value + amount)  # Ensure value doesn't go below 0
            entry.delete(0, tk.END)
            entry.insert(0, str(new_value))
        except ValueError:
            # If current value is not a valid integer, set to 0 or amount if positive
            new_value = max(0, amount)
            entry.delete(0, tk.END)
            entry.insert(0, str(new_value))

    def bind(self, event, callback):
        if event == "save":
            self._on_save = callback
        elif event == "delete":
            self._on_delete = callback
        elif event == "close":
            self._on_close = callback

    def get_values(self):
        return {
            'name': self.fish_name_entry.get().strip(),
            'count': self.fish_count_entry.get().strip(),
            'missed': self.missed_count_entry.get().strip()
        }

    def on_save(self):
        if self._on_save:
            self._on_save()

    def on_delete(self):
        if self._on_delete:
            self._on_delete()

    def on_close(self):
        if self._on_close:
            self._on_close()
        self.destroy()

    def destroy(self):
        if self.window:
            self.window.destroy()
            self.window = None