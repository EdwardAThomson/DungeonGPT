from datetime import datetime
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

class SettingsUI:
    def __init__(self, parent_frame, party_members, on_settings_saved=None):
        self.parent_frame = parent_frame
        self.party_members = party_members
        self.on_settings_saved = on_settings_saved  # Callback for when settings are saved

        # Game Parameters
        self.difficulty_var = tk.StringVar(value="Medium")
        self.length_var = tk.StringVar(value="Medium")
        self.permadeath_var = tk.BooleanVar(value=False)

        # DM Style
        self.narrative_style_var = tk.StringVar(value="Balanced")
        self.interaction_level_var = tk.StringVar(value="Balanced")

        # Create the UI
        self.create_ui()

    def create_ui(self):
        # Game Parameters Section
        params_frame = ttk.LabelFrame(self.parent_frame, text="Game Parameters")
        params_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(params_frame, text="Dungeon Difficulty:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(params_frame, textvariable=self.difficulty_var, values=["Easy", "Medium", "Hard"]).grid(row=0, column=1, padx=5)

        ttk.Label(params_frame, text="Game Length:").grid(row=1, column=0, sticky="w")
        ttk.Combobox(params_frame, textvariable=self.length_var, values=["Short", "Medium", "Long"]).grid(row=1, column=1, padx=5)

        ttk.Label(params_frame, text="Permadeath:").grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(params_frame, variable=self.permadeath_var).grid(row=2, column=1, padx=5)

        # DM Style Section
        dm_style_frame = ttk.LabelFrame(self.parent_frame, text="Dungeon Master Style")
        dm_style_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(dm_style_frame, text="Narrative Style:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(dm_style_frame, textvariable=self.narrative_style_var, values=["Humorous", "Serious", "Mysterious"]).grid(row=0, column=1, padx=5)

        ttk.Label(dm_style_frame, text="Interaction Level:").grid(row=1, column=0, sticky="w")
        ttk.Combobox(dm_style_frame, textvariable=self.interaction_level_var, values=["Minimal", "Balanced", "Story-Driven"]).grid(row=1, column=1, padx=5)

        # Save/Load Buttons
        buttons_frame = ttk.Frame(self.parent_frame)
        buttons_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Save settings
        save_button = ttk.Button(buttons_frame, text="Save & Proceed", command=self.save_game)
        save_button.grid(row=0, column=0, padx=5, pady=5)

        # Load Settings
        load_button = ttk.Button(buttons_frame, text="Load Settings", command=self.load_game)
        load_button.grid(row=0, column=1, padx=5, pady=5)

    def save_game(self):
        """Save the current game settings and party."""

        # Generate a unique filename using a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # save_file = f"saves/game_{timestamp}.json" ### old filename setup

        base_filename = f"saves/game_{timestamp}"

        # Settings file path
        save_file = f"{base_filename}.json"

        # Chat history file path
        chat_file = f"{base_filename}_chat.json"

        # Data for the save file
        save_data = {
            "party_members": self.party_members,
            "settings": {
                "difficulty": self.difficulty_var.get(),
                "length": self.length_var.get(),
                "permadeath": self.permadeath_var.get(),
                "narrative_style": self.narrative_style_var.get(),
                "interaction_level": self.interaction_level_var.get(),
            },
            "chat_file": chat_file,
        }

        # print("Save data : ")
        # print(save_data)
        # print("Chat file will go here : ")
        # print(save_data["chat_file"])
        # print("Now saving the settings....")
        # Ensure save directory exists
        os.makedirs("saves", exist_ok=True)

        try:
            with open(save_file, "w") as save_settings_file:
                json.dump(save_data, save_settings_file, indent=4)


            messagebox.showinfo("Success", f"Game settings saved successfully as {save_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the game: {e}")


        # Save to file
        #with open(save_file, "w") as f:
        #    json.dump(save_data, f, indent=4)

        # print(f"Game saved successfully as {save_file}!")
        #messagebox.showinfo("Save Successful", f"Game settings saved successfully as: {save_file}!")

        # Trigger callback if provided
        if self.on_settings_saved:
            self.on_settings_saved(save_file)


    def load_game(self):
        """Load a saved game."""
        # File selection dialog
        save_file = tk.filedialog.askopenfilename(initialdir="saves", title="Select Save File",
                                                  filetypes=(("JSON Files", "*.json"),))
        if not save_file:
            return

        # Load data
        try:
            with open(save_file, "r") as f:
                save_data = json.load(f)

            # Apply settings
            settings = save_data.get("settings", {})
            self.difficulty_var.set(settings.get("difficulty", "Medium"))
            self.length_var.set(settings.get("length", "Medium"))
            self.permadeath_var.set(settings.get("permadeath", False))
            self.narrative_style_var.set(settings.get("narrative_style", "Balanced"))
            self.interaction_level_var.set(settings.get("interaction_level", "Balanced"))

            # Update party members (Optional: Display in the UI)
            self.party_members = save_data.get("party_members", [])
            messagebox.showinfo("Load Successful", "Game loaded successfully!")
        except Exception as e:
            messagebox.showerror("Load Error", f"An error occurred while loading the game: {e}")
