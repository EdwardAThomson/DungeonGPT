import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox
import json
import os
from PIL import Image, ImageTk
from character_creation import CharacterCreatorUI
from party_selection import PartySelectionUI
from chat_interface import ChatInterfaceUI
from settings_tab import SettingsUI

class DungeonGPT:
    def __init__(self, root):
        self.root = root
        self.root.title("DungeonGPT")
        self.root.geometry("1220x1200")   # width x length

        # Configure the root window to expand
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create a canvas and scrollbar
        canvas = tk.Canvas(root)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Layout canvas and scrollbar using grid
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Bind the canvas to update its scrollable region
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Add the notebook inside the scrollable frame
        self.notebook = ttk.Notebook(scrollable_frame)
        self.notebook.pack(expand=True, fill="both")

        # Tab 0: Start Game
        self.start_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.start_frame, text="Start Game")
        self.add_start_menu_options()

        # Tab 1: Character Creation
        self.create_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.create_frame, text="Character Creation")
        self.create_ui = CharacterCreatorUI(self.create_frame, update_party_callback=self.update_party_tab)

        # Tab 2: Select Party
        self.party_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.party_frame, text="Select Party")
        self.party_ui = PartySelectionUI(self.party_frame, on_party_selected=self.open_settings_tab)

        # Tab 3: Settings
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Settings")
        self.settings_ui = SettingsUI(self.settings_frame, party_members=[], on_settings_saved=self.initialize_chat_tab)

        # Tab 4: Chat Interface
        self.chat_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.chat_frame, text="Chat Interface")
        self.chat_interface_ui = None

    def add_start_menu_options(self):
        """Add New Game and Load Game options to the Start Game tab."""
        # Add an image at the top of the tab
        try:
            image_path = "pictures/through_the_forest.webp"  # Update this with your image path
            img = Image.open(image_path)
            img = img.resize((600, 600))  # Resize as needed
            photo = ImageTk.PhotoImage(img)

            image_label = ttk.Label(self.start_frame, image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection
            image_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading image: {e}")


        start_label = ttk.Label(self.start_frame, text="Welcome to DungeonGPT!", font=("Helvetica", 16))
        start_label.pack(pady=20)

        new_game_button = ttk.Button(self.start_frame, text="New Game", command=self.start_new_game)
        new_game_button.pack(pady=10)

        load_game_button = ttk.Button(self.start_frame, text="Load Game", command=self.load_existing_game)
        load_game_button.pack(pady=10)

    def start_new_game(self):
        """Navigate to the character creation tab."""
        self.notebook.select(self.create_frame)

    def load_existing_game(self):
        """Open a file dialog to load a saved game."""

        print("Loading game....")
        file_path = filedialog.askopenfilename(
            title="Select a saved game file",
            initialdir="saves",  # Set the default directory to /saves
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not file_path:
            return  # User canceled

        # Load the saved game
        try:
            with open(file_path, "r") as f:
                saved_game = json.load(f)

            # Assume saved_game includes characters, settings, and conversation history
            party_members = saved_game.get("party_members", [])
            settings = saved_game.get("settings", {})

            # print("Loaded party members and settings.")
            chat_file = saved_game.get("chat_file", None)
            # print(f"The chat file is: {chat_file}")
            # print(f"Chat file exists? {os.path.exists(chat_file)}")

            # Pass data to the chat interface
            self.chat_interface_ui = ChatInterfaceUI(
                self.chat_frame, party_members=party_members, settings=settings, chat_file=chat_file
            )

            # print("Chat interface UI created")

            # Load chat history if chat file exists
            chat_history = []
            if chat_file and os.path.exists(chat_file):
                with open(chat_file, "r") as f:
                    chat_history = json.load(f)

            # print("Chat history loaded")
            # print(chat_history)

            self.chat_interface_ui.load_conversation(chat_history)

            # Navigate to the chat interface tab
            self.notebook.select(self.chat_frame)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the game: {e}")

    def update_party_tab(self):
        """Update the party selection tab."""
        self.party_ui.update_characters()

    def open_settings_tab(self, selected_party=None):
        """Open the settings tab with the selected party."""
        self.notebook.select(self.settings_frame)
        self.settings_ui.party_members = selected_party        # Pass the selected party to the chat interface

    def initialize_chat_tab(self, save_file):
        """Initialize the chat interface after settings are saved."""
        # Load settings and party members from the save file
        with open(save_file, "r") as f:
            save_data = json.load(f)

        print("opened saved party file:")
        print(save_file)
        party_members = save_data.get("party_members", [])
        settings = save_data.get("settings", {})
        chat_file = save_data.get("chat_file", None)

        # print(f"The chat file is: {chat_file}")

        # Initialize the chat interface with both settings and party
        self.chat_interface_ui = ChatInterfaceUI(self.chat_frame, party_members, settings, chat_file)

        # Switch to the chat tab
        self.notebook.select(self.chat_frame)


    def on_settings_saved(self, save_file):
        print(f"Game saved to: {save_file}")




def main():
    root = tk.Tk()
    app = DungeonGPT(root)
    root.mainloop()

if __name__ == "__main__":
    main()
