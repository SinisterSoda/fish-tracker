import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class GraphView:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.window = tk.Toplevel(self.root)
        self.window.title("Session Graph")
        self.window.geometry("900x750")

        # Add sort order tracking
        self.current_sort = None
        self.reverse_sort = False
        
        self.window.protocol("WM_DELETE_WINDOW", self.destroy)

        self.create_widgets()

    def create_widgets(self):

        sort_frame = tk.Frame(self.window)
        sort_frame.pack(fill=tk.X)

        # Add sort buttons
        sort_options = [
            ("Count", "count"),
            ("Missed", "missed"),
            ("Percentage", "percentage"),
            ("Number Seen", "number_seen"),
            ("Catch %", "catch_percentage"),
            ("Seen %", "seen_percentage")
        ]

        for label, attr in sort_options:
            btn = tk.Button(sort_frame, text=f"Sort by {label}",
                          command=lambda a=attr: self.sort_and_refresh(a))
            btn.pack(side=tk.LEFT, padx=2)

        self.notebook = tk.ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_graphs()

    def create_graphs(self):
        # Move graph creation code here to avoid duplication
        self.create_graph("Count", "count")
        self.create_graph("Missed", "missed")
        self.create_graph("Percentage", "percentage", bar_label_affix="%")
        self.create_graph("Number Seen", "number_seen")
        self.create_graph("Catch Percentage", "catch_percentage", bar_label_affix="%")
        self.create_graph("Seen Percentage", "seen_percentage", bar_label_affix="%")

    def sort_and_refresh(self, attribute):
        # Toggle sort direction if clicking same attribute
        if self.current_sort == attribute:
            self.reverse_sort = not self.reverse_sort
        else:
            self.current_sort = attribute
            self.reverse_sort = False
            
        # Sort the data
        self.data.sort(
            key=lambda x: self.get_attribute_value(x, attribute),
            reverse=self.reverse_sort
        )
        
        # Clear and recreate graphs
        for widget in self.notebook.winfo_children():
            widget.destroy()
        self.create_graphs()

    def create_graph(self, title, attribute, max_label_length=10, bottom_margin=0.2, bar_label_affix=""):
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text=title)

        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)

        names = [fish['name'] for fish in self.data]
        values = [self.get_attribute_value(fish, attribute) for fish in self.data]
        bars = ax.bar(names, values)
        ax.set_title(f"{title} Graph")
        ax.set_xlabel("Fish")
        ax.set_ylabel(title)
        
        # Set y-axis limits to start from 0
        ax.set_ylim(bottom=0)
        
        # Adjust x-axis labels
        ax.set_xticklabels(names, rotation=0, ha='center')
        fig.tight_layout()
        
        # Word wrap long labels
        wrapped_labels = []
        for name in names:
            words = name.split()
            lines = []
            current_line = ""
            for word in words:
                if len(current_line) + len(word) <= max_label_length:
                    current_line += " " + word if current_line else word
                else:
                    if current_line:
                        lines.append(current_line)
                    if len(word) > max_label_length:
                        lines.extend([word[i:i+max_label_length] for i in range(0, len(word), max_label_length)])
                    else:
                        current_line = word
            if current_line:
                lines.append(current_line)
            wrapped_labels.append('\n'.join(lines))
        ax.set_xticklabels(wrapped_labels)
        
        # Adjust bottom margin to accommodate wrapped labels
        plt.subplots_adjust(bottom=bottom_margin)

        # display values inside the bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}{bar_label_affix}',
                    ha='center', va='bottom')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        

    def get_attribute_value(self, fish, attribute):
        if attribute == "count":
            return fish['count']
        elif attribute == "missed":
            return fish.get('missed', 0)
        elif attribute == "percentage":
            return float(fish['percentage'].strip('%'))
        elif attribute == "number_seen":
            return fish['count'] + fish.get('missed', 0)
        elif attribute == "catch_percentage":
            return float(fish['catch_percentage'].strip('%'))
        elif attribute == "seen_percentage":
            return float(fish['seen_percentage'].strip('%'))
        else:
            return 0
        
    def destroy(self):
        if self.window:
            self.window.destroy()
            self.window = None
        if self.notebook:
            self.notebook.destroy()
            self.notebook = None
        if self.root:
            self.root = None
        