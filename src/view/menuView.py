import tkinter as tk
from tkinter import ttk

class menuView:
    def __init__(self, root):
        self.root = root
        menu_bar = tk.Menu(root)
        
        self._new_session = None
        self._save_session = None
        self._load_session = None
        self._combine_sessions = None

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
        