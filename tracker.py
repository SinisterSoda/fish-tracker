import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json

class FishTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fish Tracker")

        self.fish_data = []

        # Create UI components
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Frame for input
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # Fish Name Entry
        self.fish_name_entry = tk.Entry(input_frame, width=20)
        self.fish_name_entry.grid(row=0, column=0, sticky="w", padx=(5, 0))
        self.fish_name_entry.insert(0, "Fish Name")

        # Fish Count Entry
        self.fish_count_entry = tk.Entry(input_frame, width=10)
        self.fish_count_entry.grid(row=1, column=0, sticky="w", padx=(5, 0), pady=(5, 0))
        self.fish_count_entry.insert(0, "Count")

        # Add Fish Button
        add_button = tk.Button(input_frame, text="Add Fish", command=self.add_fish)
        add_button.grid(row=2, column=0, sticky="w", padx=(5, 0), pady=(5, 0))

        # Label for editing instructions
        edit_label = tk.Label(self.root, text="Double-click a fish entry to edit.")
        edit_label.pack(pady=(10, 0))

        # Treeview for displaying fish data
        self.tree = ttk.Treeview(self.root, columns=("Fish", "Count"), show="headings")
        self.tree.heading("Fish", text="Fish")
        self.tree.heading("Count", text="Count")
        self.tree.pack(pady=10)

        # Bind double-click event to edit fish
        self.tree.bind("<Double-1>", self.edit_fish)

        # Treeview for displaying percentages
        self.percentage_tree = ttk.Treeview(self.root, columns=("Fish", "Count", "Percentage"), show="headings")
        self.percentage_tree.heading("Fish", text="Fish")
        self.percentage_tree.heading("Count", text="Count")
        self.percentage_tree.heading("Percentage", text="Percentage")
        self.percentage_tree.pack(pady=(10, 30), padx=(10, 10))

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save Session", command=self.save_session)
        file_menu.add_command(label="Load Session", command=self.load_session)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

    def add_fish(self):
        fish_name = self.fish_name_entry.get().strip()
        try:
            fish_count = int(self.fish_count_entry.get().strip())
            if fish_name and fish_count > 0:
                self.fish_data.append((fish_name, fish_count))
                self.update_trees()  # Update and sort trees
                self.fish_name_entry.delete(0, tk.END)
                self.fish_count_entry.delete(0, tk.END)
                self.fish_name_entry.focus()
            else:
                messagebox.showwarning("Input Error", "Please enter a valid fish name and count.")
        except ValueError:
            messagebox.showwarning("Input Error", "Count must be a valid integer.")

    def edit_fish(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item)
        fish_name, fish_count = item['values'][0], item['values'][1]

        # Create edit pop-up
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Fish")

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
                if new_fish_name and new_fish_count > 0:
                    index = self.tree.index(selected_item)
                    self.fish_data[index] = (new_fish_name, new_fish_count)
                    self.update_trees()  # Update and sort trees
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Input Error", "Please enter a valid fish name and count.")
            except ValueError:
                messagebox.showwarning("Input Error", "Count must be a valid integer.")

        save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def update_trees(self):
        # Clear and sort the fish data
        self.fish_data.sort(key=lambda x: x[0])  # Sort by fish name
        self.tree.delete(*self.tree.get_children())
        for fish, count in self.fish_data:
            self.tree.insert("", "end", values=(fish, count))

        self.update_percentages()

    def update_percentages(self):
        for item in self.percentage_tree.get_children():
            self.percentage_tree.delete(item)

        if not self.fish_data:
            return

        total_count = sum(count for _, count in self.fish_data)
        percentages = [(fish, count, (count / total_count) * 100) for fish, count in self.fish_data]

        percentages.sort(key=lambda x: x[0])  # Sort percentages by fish name

        for fish, count, percentage in percentages:
            self.percentage_tree.insert("", "end", values=(fish, count, f"{percentage:.2f}%"))

        self.percentage_tree.insert("", "end", values=("Total", total_count, "100%"))

    def save_session(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        with open(file_path, 'w') as json_file:
            json.dump(self.fish_data, json_file)

    def load_session(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        with open(file_path, 'r') as json_file:
            self.fish_data = json.load(json_file)

        self.update_trees()  # Update and sort trees after loading

if __name__ == "__main__":
    root = tk.Tk()
    app = FishTrackerApp(root)
    root.mainloop()
