import tkinter as tk
import json
from tkinter import ttk, messagebox
from ai_helper import send_prompt

class CharacterCreatorUI:
    def __init__(self, parent, update_party_callback=None):
        self.parent = parent
        self.update_party_callback = update_party_callback

        # This will store all created characters in memory.
        # You could replace this with saving to a file, a DB, or an API call.
        self.created_characters = []


        # Main frame (for neat layout)
        self.main_frame = ttk.Frame(parent)
        self.main_frame.grid(row=0, column=0, sticky=tk.W)

        # 1. Character Name
        ttk.Label(self.main_frame, text="Character Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.name_var, width=20).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # 2. Character Gender
        ttk.Label(self.main_frame, text="Gender:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.gender_var = tk.StringVar()
        gender_options = ["Male", "Female"]
        self.gender_dropdown = ttk.OptionMenu(self.main_frame, self.gender_var, gender_options[0], *gender_options)
        self.gender_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # 3. Character Race
        ttk.Label(self.main_frame, text="Race:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.race_var = tk.StringVar()
        # characterRaces = ["Human", "Dwarf", "Elf", "Halfling", "Dragonborn", "Gnome", "Half-Elf", "Half-Orc", "Tiefling"];
        race_options = ["Human", "Elf", "Dwarf", "Halfling"]
        self.race_dropdown = ttk.OptionMenu(self.main_frame, self.race_var, race_options[0], *race_options)
        self.race_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # 4. Character Class
        ttk.Label(self.main_frame, text="Class:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.class_var = tk.StringVar()
        # characterClasses = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
        class_options = ["Barbarian", "Fighter", "Rogue", "Wizard", "Paladin", "Cleric", "Ranger", "Monk", "Druid"]
        self.class_dropdown = ttk.OptionMenu(self.main_frame, self.class_var, class_options[0], *class_options)
        self.class_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        # 5. Level
        ttk.Label(self.main_frame, text="Level:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.level_var = tk.IntVar(value=1)
        ttk.Spinbox(self.main_frame, from_=1, to=20, textvariable=self.level_var, width=5).grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        # 6. Alignment
        ttk.Label(self.main_frame, text="Alignment:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.alignment_var = tk.StringVar()
        alignment_options = [
            "Lawful Good",
            "Neutral Good",
            "Chaotic Good",
            "Lawful Neutral",
            "True Neutral",
            "Chaotic Neutral",
            "Lawful Evil",
            "Neutral Evil",
            "Chaotic Evil",
        ]
        self.alignment_dropdown = ttk.OptionMenu(self.main_frame, self.alignment_var, alignment_options[0], *alignment_options)
        self.alignment_dropdown.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        # 7. Background
        ttk.Label(self.main_frame, text="Background:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.background_text = tk.Text(self.main_frame, width=30, height=5)
        self.background_text.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

        # 8. Stats Frame
        stats_frame = ttk.LabelFrame(self.main_frame, text="Stats")
        stats_frame.grid(row=7, column=1, columnspan=2, padx=5, pady=10, sticky=tk.W)

        # Create dictionary to hold stat variables
        self.stats_vars = {
            "Strength": tk.IntVar(value=10),
            "Dexterity": tk.IntVar(value=10),
            "Constitution": tk.IntVar(value=10),
            "Intelligence": tk.IntVar(value=10),
            "Wisdom": tk.IntVar(value=10),
            "Charisma": tk.IntVar(value=10),
        }

        row_index = 0
        for stat_name, var in self.stats_vars.items():
            ttk.Label(stats_frame, text=f"{stat_name}:").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=5)
            ttk.Spinbox(stats_frame, from_=1, to=20, textvariable=var, width=5).grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1


        # PROFILE PICTURES
        pics_frame = ttk.LabelFrame(self.main_frame, text="Profile Picture")
        pics_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky=tk.W)

        # Paths
        # Store them in a list  (include correct paths plus .png/.jpg )
        path="pictures/"
        profile_pics = [f"{path}barbarian.png", f"{path}wizard.png", f"{path}ranger.png",
                        f"{path}fighter.png", f"{path}bard.png", f"{path}cleric.png", f"{path}druid.png",
                        f"{path}paladin.png"]

        # IMPORTANT: Store image objects in a list or dict so they're not garbage-collected
        self.profile_images = []
        self.profile_pic_var = tk.StringVar()

        # We'll default to the first picture
        self.profile_pic_var.set(profile_pics[0])

        # Arrange pictures into a grid with 3 columns max
        # row, col = 0, 0
        max_columns = 3  # Maximum number of columns in the grid

        # Create a row of radio buttons, each with the corresponding image
        for i, pic_path in enumerate(profile_pics):
            try:
                # Load and possibly resize
                img = tk.PhotoImage(file=pic_path)
                # Example resizing if your images are big
                # img = img.subsample(1, 1)
            except Exception as e:
                # If the image fails to load, we can fall back
                messagebox.showwarning("Image Error", f"Could not load {pic_path}. {e}")
                continue

            self.profile_images.append(img)

            # Calculate row and column for the grid
            row = i // max_columns
            column = i % max_columns

            rad = ttk.Radiobutton(
                pics_frame,
                image=self.profile_images[-1],
                variable=self.profile_pic_var,
                value=pic_path
            )
            # rad.grid(row=0, column=i, padx=5, pady=5)
            rad.grid(row=row, column=column, padx=5, pady=5)



        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=10)

        save_btn = ttk.Button(button_frame, text="Save Character", command=self.save_character)
        save_btn.pack(side=tk.LEFT, padx=5)

        show_btn = ttk.Button(button_frame, text="View Characters", command=self.show_all_characters)
        show_btn.pack(side=tk.LEFT, padx=5)

        gen_frame = ttk.Frame(self.main_frame)
        gen_frame.grid(row=10, column=1, columnspan=2, pady=10, sticky=tk.W)

        auto_btn = ttk.Button(gen_frame, text="Auto Generate", command=self.auto_generate)
        # auto_btn.pack(side=tk.LEFT, padx=5)
        auto_btn.grid(row=0, column=0, padx=5, pady=5)


    def save_character(self):
        """Collects all data from the form and adds it to 'created_characters' list."""
        print("trying to save character")

        name = self.name_var.get().strip()
        gender = self.gender_var.get().strip()
        race = self.race_var.get().strip()
        char_class = self.class_var.get().strip()
        level = self.level_var.get()
        alignment = self.alignment_var.get().strip()
        background = self.background_text.get("1.0", tk.END).strip()
        profile_pic = self.profile_pic_var.get()

        # If you want to ensure name is provided:
        if not name:
            messagebox.showwarning("Missing Name", "Please provide a character name.")
            return

        stats = {
            stat_name: var.get() for stat_name, var in self.stats_vars.items()
        }

        new_character = {
            "name": name,
            "gender": gender,
            "race": race,
            "class": char_class,
            "level": level,
            "alignment": alignment,
            "background": background,
            "stats": stats,
            "profile_pic": profile_pic
        }

        self.created_characters.append(new_character)

        # (Optional) Clear fields after creation
        # self.name_var.set("")
        # self.background_text.delete("1.0", tk.END)
        # for stat_var in self.stats_vars.values():
        #    stat_var.set(10)

        # Save to file
        char_path="characters/"

        len_cc = len(self.created_characters)

        print(self.created_characters[0])  # check here.
        print(self.created_characters[len_cc - 1])


        print(f"Saving character '{name}' to {char_path}")

        with open(f"{char_path}{name}_Level_{level}_{char_class}.json", "w") as char_file:
            json.dump(self.created_characters[len_cc - 1], char_file)   # check the [0] too. Maybe messing up?

        messagebox.showinfo("Success", f"Character '{name}' saved successfully!")

        # Update the party selection tab with the new character
        if self.update_party_callback:
            self.update_party_callback()

    def auto_generate(self):
        """Auto-generates a character via the OpenAI API."""
        self.clear_form()  # Clear existing form data
        print("Auto-generating character...")

        # make API request
        try:

            prompt = (
                f"Please create a D&D character with the following characteristics: \n\n"
                f"name\n"
                f"gender (Only Male or Female)\n"
                f"race\n"
                f"class\n"
                f"level\n"
                f"alignment\n"
                f"background\n"
                f"stats (Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma).\n\n"
                f"Please respond in valid JSON format with no backticks."
            )

            # print(prompt)

            generated_character = send_prompt(prompt, model="gpt-4o", max_tokens=16384, temperature=0.7,
                                              role_description="You are a dungeon master. You will create original text only.")
            # print(generated_character)

            # Show a success message
            messagebox.showinfo("Success", f"Character auto-generated successfully!" )

            # Parse the JSON response
            try:
                character_data = json.loads(generated_character)
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"Failed to parse JSON response: {str(e)}")
                return

            # Validate the JSON object (check for required fields)
            required_fields = ["name", "gender", "race", "class", "level", "alignment", "background", "stats"]
            for field in required_fields:
                if field not in character_data:
                    messagebox.showerror("Error", f"Missing required field in response: {field}")
                    return


            # Display auto-generated character in a pop-up text box
            ### Good Debugging, but don't really need. ###
            # top = tk.Toplevel(self.root)
            # top.title("New Character")

            # Use a Text widget
            # text_area = tk.Text(top, width=60, height=20)
            # text_area.pack(padx=10, pady=10)
            # text_area.insert(tk.END, generated_character)
            # text_area.insert(tk.END, f"\n\n -------  JSON Check  ------- \n\n")
            # text_area.insert(tk.END, json.dumps(character_data, indent=4))

            # Populate the form
            self.populate_form(character_data)



        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating a character: {str(e)}")



    def populate_form(self, character_data):
        """Populates the character creation form with the given character data."""

        try:
            # Clear form first
            self.clear_form()

            # Map JSON data to the form fields
            self.name_var.set(character_data.get("name", ""))
            self.gender_var.set(character_data.get("gender", "Male"))
            self.race_var.set(character_data.get("race", "Human"))
            self.class_var.set(character_data.get("class", "Fighter"))
            self.level_var.set(character_data.get("level", 1))
            self.alignment_var.set(character_data.get("alignment", "True Neutral"))
            self.background_text.delete("1.0", tk.END)
            self.background_text.insert("1.0", character_data.get("background", ""))

            # Populate stats
            stats = character_data.get("stats", {})
            for stat_name, var in self.stats_vars.items():
                var.set(stats.get(stat_name, 10))


            messagebox.showinfo("Success", "Form populated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while populating the form: {str(e)}")


    def show_all_characters(self):
        """Opens a new window that lists all created characters."""
        if not self.created_characters:
            messagebox.showinfo("No Characters", "No characters have been created yet.")
            return

        top = tk.Toplevel(self.parent)
        top.title("All Characters")

        # Use a Text widget or a Listbox to display all characters
        text_area = tk.Text(top, width=60, height=20)
        text_area.pack(padx=10, pady=10)

        for idx, char in enumerate(self.created_characters, start=1):
            text_area.insert(tk.END, f"Character {idx}:\n")
            text_area.insert(tk.END, f"  Name: {char['name']}\n")
            text_area.insert(tk.END, f"  Gender: {char['gender']}\n")
            text_area.insert(tk.END, f"  Race: {char['race']}\n")
            text_area.insert(tk.END, f"  Class: {char['class']}\n")
            text_area.insert(tk.END, f"  Level: {char['level']}\n")
            text_area.insert(tk.END, f"  Alignment: {char['alignment']}\n")
            text_area.insert(tk.END, f"  Background: {char['background']}\n")
            text_area.insert(tk.END, "  Stats:\n")
            for stat_name, value in char["stats"].items():
                text_area.insert(tk.END, f"    {stat_name}: {value}\n")
            text_area.insert(tk.END, "\n" + "-"*40 + "\n\n")

    def clear_form(self):
        """Clears all fields in the form."""
        self.name_var.set("")
        self.gender_var.set("")
        self.race_var.set("")
        self.class_var.set("")
        self.level_var.set(1)
        self.alignment_var.set("")
        self.background_text.delete("1.0", tk.END)
        for var in self.stats_vars.values():
            var.set(10)
        self.profile_pic_var.set("")



def main():
    root = tk.Tk()
    app = CharacterCreatorUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
