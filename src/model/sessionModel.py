import json
import os
from tkinter import filedialog

class sessionModel:
    def __init__(self, data, water_type, bait_type):
        self.fish_data = data
        self.water_type = water_type
        self.bait_type = bait_type
        
    def is_empty(self):
        return len(self.fish_data) < 1
    
    def save_session(self):
        self.sessions_folder = os.path.join(os.getcwd(), "sessions")
        file_path = filedialog.asksaveasfilename(defaultextension=".json", initialdir=self.sessions_folder, 
                                                   filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        session_data = {
            "water_type": self.water_type,
            "bait_type": self.bait_type,
            "fish_data": self.fish_data
        }
        
        with open(file_path, 'w') as f:
            json.dump(session_data, f, indent=4)
            
    def clear(self):
        self.fish_data.clear()  # Clear the data
        self.water_type = "Unspecified/Mixed"
        self.bait_type = "Unspecified/Mixed"
        
    def fish_index(self, fish_name):
        for index, fish in enumerate(self.fish_data):
            if fish['name'].lower() == fish_name.lower():  # Case insensitive comparison
                return index
        return -1  # Return -1 if the fish is not found
        
    def add_fish(self, fish):
        if 'missed' not in fish:
            fish['missed'] = 0
        self.fish_data.append(fish)
        
    def update_at(self, index, f):
        self.fish_data[index] = f
        
    @staticmethod
    def load_session():
        sessions_folder = os.path.join(os.getcwd(), "sessions")
        file_path = filedialog.askopenfilename(defaultextension=".json", initialdir=sessions_folder, 
                                                filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        return sessionModel.load_file(file_path)
    
    @staticmethod
    def load_file(file_path):
        with open(file_path, 'r') as f:
            session_data = json.load(f)
        
          
        wt = session_data.get("water_type", "Unspecified/Mixed")
        bt = session_data.get("bait_type", "Unspecified/Mixed")
        fd = session_data.get("fish_data", [])
        # Ensure each fish has a 'missed' value
        for fish in fd:
            if 'missed' not in fish:
                fish['missed'] = 0
        
        # Combine fish entries with the same name
        combined_fish_data = {}
        for fish in fd:
            name = fish['name']
            if name in combined_fish_data:
                combined_fish_data[name]['count'] += fish['count']
                combined_fish_data[name]['missed'] += fish['missed']
            else:
                combined_fish_data[name] = fish.copy()
        
        # Convert the combined data back to a list
        fd = list(combined_fish_data.values())
        return sessionModel(fd, wt, bt)