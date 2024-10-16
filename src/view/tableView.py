from tkinter import ttk

class tableView:
    def __init__(self, root, data):
        self.data = data
        self.root = root
        
        # Treeview for displaying fish data with percentages
        self.tree = ttk.Treeview(self.root, columns=("Fish", "Count", "Percentage"), show="headings")
        self.tree.heading("Fish", text="Fish", command=lambda: self.sort_column("Fish"))
        self.tree.heading("Count", text="Count", command=lambda: self.sort_column("Count"))
        self.tree.heading("Percentage", text="Percentage", command=lambda: self.sort_column("Percentage"))
        self.tree.grid(row=9, pady=(10, 30), padx=(10, 10))
        self.sort_order = {"Fish": True, "Count": True, "Percentage": True}
        
        self.bind("<Double-1>", self.sort_column)
        
        self.update_tree(self.data)
        
    def bind(self, cmd, fn):
        # Bind bind event to value
        self.tree.bind(cmd, fn)#"<Double-1>"
        
    def update_tree(self, new_data):
        self.data = new_data
        # Clear the tree
        self.tree.delete(*self.tree.get_children())

        if not self.data:
            self.tree.insert("", "end", values=("Total", 0, "-----"))
            return

        total_count = sum(item['count'] for item in self.data)
        for fish in self.data:
            percentage = (fish['count'] / total_count) * 100 if total_count > 0 else 0
            self.tree.insert("", "end", values=(fish['name'], fish['count'], f"{percentage:.2f}%"))

        # Add Total row at the bottom
        self.tree.insert("", "end", values=("Total", total_count, "-----"))
        
    def sort_column(self, col):
        if col in self.sort_order:
            k = "name"
            if col == "Fish":
                k = "name"
            elif col == "Count":
                k = "count"

            self.sort_order[col] = not self.sort_order[col]
            ascending = self.sort_order[col]
            s = sum(item['count'] for item in self.data)
            self.data.sort(key=lambda x: (x[k] if col != "Percentage" else x['count']/s), 
                                reverse=not ascending)
            self.update_tree(self.data)  # Refresh the tree view with sorted data
            
            
    def selection(self):
        return self.tree.selection()
    
    def index(self, index):
        return self.tree.index(index)