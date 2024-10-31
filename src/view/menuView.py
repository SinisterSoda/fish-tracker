import tkinter as tk
from tkinter import ttk

import platform

class menuView:
    def __init__(self, root):
        self.root = root
        menu_bar = tk.Menu(root)
        
        self._new_session = None
        self._save_session = None
        self._load_session = None
        self._combine_sessions = None
        self._graph_current_session = None
        self._graph_other_session = None 

        self.modifier_key = "Command" if platform.system() == "Darwin" else "Ctrl"
        self.command_key = "Command" if platform.system() == "Darwin" else "Control"
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Session", command=self.new_session, accelerator=f"{self.modifier_key}+N")
        file_menu.add_command(label="Save Session", command=self.save_session, accelerator=f"{self.modifier_key}+S") 
        file_menu.add_command(label="Open Session", command=self.load_session, accelerator=f"{self.modifier_key}+O")
        file_menu.add_command(label="Combine Sessions", command=self.combine_sessions, accelerator=f"{self.modifier_key}+Shift+O")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)

        # Compare menu
        compare_menu = tk.Menu(menu_bar, tearoff=0)
        compare_menu.add_command(label="Compare Sessions", command=self.compare_sessions, accelerator=f"{self.modifier_key}+C")
        menu_bar.add_cascade(label="Compare", menu=compare_menu)

        # Graph menu
        graph_menu = tk.Menu(menu_bar, tearoff=0)
        graph_menu.add_command(label="Graph Current Session", command=self.graph_current_session, accelerator=f"{self.modifier_key}+G")
        graph_menu.add_command(label="Compare Graphs", command=self.graph_other_session, accelerator=f"{self.modifier_key}+Shift+G")
        menu_bar.add_cascade(label="Graph", menu=graph_menu)


        # Add these bindings after creating the menu
        self.root.bind(f"<{self.command_key}-n>", lambda e: self.new_session())
        self.root.bind(f"<{self.command_key}-s>", lambda e: self.save_session())
        self.root.bind(f"<{self.command_key}-o>", lambda e: self.load_session())
        self.root.bind(f"<{self.command_key}-O>", lambda e: self.combine_sessions())

        self.root.bind(f"<{self.command_key}-g>", lambda e: self.graph_current_session())
        self.root.bind(f"<{self.command_key}-G>", lambda e: self.graph_other_session())


        

        self.root.config(menu=menu_bar)
        
    def bind(self, cmd, fn):
        if cmd == "new":
            self._new_session = fn
        elif cmd == "save":
            self._save_session = fn
        elif cmd == "load":
            self._load_session = fn
        elif cmd == "combine":
            self._combine_sessions = fn
        elif cmd == "compare":
            self._compare_sessions = fn
        elif cmd == "graph":
            self._graph_current_session = fn
        elif cmd == "graph_other":  # New binding
            self._graph_other_session = fn
    
    def new_session(self):
        if self._new_session is not None and callable(self._new_session):
            self._new_session()

    def save_session(self):
        if self._save_session is not None and callable(self._save_session):
            self._save_session()

    def load_session(self):
        if self._load_session is not None and callable(self._load_session):
            self._load_session()

    def combine_sessions(self):
        if self._combine_sessions is not None and callable(self._combine_sessions):
            self._combine_sessions()
            
    def compare_sessions(self):
        if self._compare_sessions is not None and callable(self._compare_sessions):
            self._compare_sessions()

    def graph_current_session(self):
        if self._graph_current_session is not None and callable(self._graph_current_session):
            self._graph_current_session()

    def graph_other_session(self):
        if self._graph_other_session is not None and callable(self._graph_other_session):
            self._graph_other_session()
        