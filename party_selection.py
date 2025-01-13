import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

class PartySelectionUI:
    def __init__(self, parent_frame, char_path="characters/", on_party_selected=None):
        self.char_path = char_path
        self.parent_frame = parent_frame
        self.on_party_selected = on_party_selected
        self.character_grid = ttk.Frame(parent_frame)
        self.character_grid.grid(row=0, column=0, padx=10, pady=10)

        self.party_selection = []
        self.selected_party = []

        # Add a button to confirm selection
        confirm_btn = ttk.Button(parent_frame, text="Confirm Party", command=self.confirm_party)
        confirm_btn.grid(row=1, column=0, pady=10)

        self.load_characters_to_grid()

    def update_characters(self):
        """Refresh the character grid."""
        self.load_characters_to_grid()

    def load_characters_to_grid(self):
        """Load and display characters in the grid."""
        # Clear previous grid
        for widget in self.character_grid.winfo_children():
            widget.destroy()

        files = [f for f in os.listdir(self.char_path) if f.endswith(".json")]

        row, col = 0, 0
        max_columns = 4  # Adjust as needed

        for file in files:
            try:
                with open(os.path.join(self.char_path, file), "r") as f:
                    character = json.load(f)

                # Create a frame for each character
                char_frame = ttk.Frame(self.character_grid, relief="ridge", padding=5)
                char_frame.grid(row=row, column=col, padx=5, pady=5, sticky=tk.NSEW)

                # Load and display picture
                profile_pic_path = character.get("profile_pic")
                if profile_pic_path and os.path.exists(profile_pic_path):
                    try:
                        img = tk.PhotoImage(file=profile_pic_path)
                        # Resize the image if needed
                        img = img.subsample(2, 2)  # Adjust scaling factor as required
                        pic_label = ttk.Label(char_frame, image=img)
                        pic_label.image = img  # Keep a reference to avoid garbage collection
                        pic_label.grid(row=0, column=0)
                    except Exception as e:
                        print(f"Error loading image {profile_pic_path}: {e}")
                        ttk.Label(char_frame, text="No Image").grid(row=0, column=0)
                else:
                    ttk.Label(char_frame, text="No Image").grid(row=0, column=0)



                # Display name
                name_label = ttk.Label(char_frame, text=character["name"])
                name_label.grid(row=1, column=0)

                # Add a checkbox for selection
                selected_var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(char_frame, variable=selected_var)
                checkbox.grid(row=2, column=0)

                # Track the selection state
                self.party_selection.append((character, selected_var))

                # Manage grid layout
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1
            except Exception as e:
                print(f"Error loading character from {file}: {e}")

    def confirm_party(self):
         # Get selected characters
        selected_files = [os.path.join(self.char_path, f"{char['name']}_Level_{char['level']}_{char['class']}.json")
                                       #char["name"] + "_Level_" + char["level"] + "_" + char["class"] + ".json")
                          for char, var in self.party_selection if var.get()]

       #  "{char_path}{name}_Level_{level}_{char_class}.json"

        if len(selected_files) != 4:
            messagebox.showwarning("Selection Error", "Please select exactly 4 characters.")
            return

        # Save the selected party (list of file paths)
        self.selected_party = selected_files
        print("Your party has been selected successfully!")
        print(self.selected_party)

        # Notify success
        messagebox.showinfo("Party Selected", "Your party has been selected successfully!")

        # Invoke the callback only if it is set
        if self.on_party_selected is not None:
            self.on_party_selected(self.selected_party)