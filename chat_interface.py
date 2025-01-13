import tkinter as tk
from tkinter import ttk
from ai_helper import send_prompt
import json
from PIL import Image, ImageTk  # For handling images other than PNG
import os

class ChatInterfaceUI:
    def __init__(self, parent_frame, party_members, settings, chat_file):
        self.parent_frame = parent_frame
        self.party_members = party_members  # List of selected character file paths
        self.settings = settings
        self.chat_file = chat_file
        self.party_data = self.load_party_data()  # Preload party data


        self.conversation_history = []  # Stores all messages as {id, user, response}
        self.message_counter = 1  # Tracks the current message ID

        # UI
        # Split the layout into two main areas
        self.left_frame = ttk.Frame(self.parent_frame)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.right_frame = ttk.Frame(self.parent_frame, relief="solid", borderwidth=1)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Chat log
        self.chat_log = tk.Text(self.left_frame, height=40, width=100, state="disabled", wrap="word")
        self.chat_log.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.scrollbar = ttk.Scrollbar(self.left_frame, command=self.chat_log.yview)
        self.chat_log.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=2, sticky="ns")


        # Input field
        self.chat_input = tk.Entry(self.left_frame, width=50)
        self.chat_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Send button
        send_button = ttk.Button(self.left_frame, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1, padx=10, pady=10)

        # Display party members in the right frame
        self.display_party_members()

    def display_party_members(self):
        """Display the selected party members in the top-right corner."""
        # print("party members:")
        # print(self.party_members)

        for idx, character_file in enumerate(self.party_members):
            try:
                # Load character data
                with open(character_file, "r") as f:
                    character = json.load(f)

                # Create a frame for each character
                char_frame = ttk.Frame(self.right_frame, relief="ridge", padding=5)
                char_frame.grid(row=idx, column=0, padx=5, pady=5, sticky="nsew")

                profile_pic_path = character.get("profile_pic")

                # Display picture
                if "profile_pic" in character and os.path.exists(character["profile_pic"]):
                    img = Image.open(character["profile_pic"])
                    img = img.resize((100, 100))  # Resize image  # ,  Image.ANTIALIAS
                    photo = ImageTk.PhotoImage(img)
                    pic_label = ttk.Label(char_frame, image=photo)
                    pic_label.image = photo  # Keep reference to avoid garbage collection
                    pic_label.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
                else:
                    ttk.Label(char_frame, text="No Image").grid(row=0, column=0, rowspan=2)

                # Display name, level, and class
                ttk.Label(char_frame, text=f"Name: {character['name']}").grid(row=0, column=1, sticky="w")
                ttk.Label(char_frame, text=f"Level: {character['level']}").grid(row=1, column=1, sticky="w")
                ttk.Label(char_frame, text=f"Class: {character['class']}").grid(row=2, column=1, sticky="w")
            except Exception as e:
                print(f"Error loading character: {e}")


    def load_party_data(self):
        """Load party member data into memory."""
        party_data = []
        for character_file in self.party_members:
            try:
                with open(character_file, "r") as f:
                    character = json.load(f)
                    party_data.append(character)
            except Exception as e:
                print(f"Error loading character: {e}")
        return party_data

    def prepare_prompt(self, user_message):
        """Prepare the prompt for OpenAI."""
        # Include settings and context if needed
        context = f"Game Settings: {json.dumps(self.settings)}\n"
        context += "Party Members:\n"
        for character in self.party_data:
            context += f"- {character['name']} (Level {character['level']}, {character['class']})\n"

        # Get recent messages
        recent_history = self.get_recent_history(max_tokens=15000)
        history = "\n".join(
            f"Player: {entry['user']}\nDungeon Master: {entry['response']}" for entry in recent_history
        )

        # Combine context, history, and the new user message
        # context == game settings and party members
        prompt = (
            f"{context}\n"
            f"Conversation History:\n{history}\n"
            f"\nDungeon Master, please respond to the player's message:\n\n"
            f"Player: {user_message}\nDM:"
        )

        # print("prompt:")
        # print(prompt)
        return prompt

    def display_response(self, response):
        """Display the response from the Dungeon Master."""
        # Assuming `response` contains the reply text directly
        reply = response.strip()

        # Append the reply to the chat log
        self.chat_log.configure(state="normal")
        # self.chat_log.insert(tk.END, "\n")  # Add a blank line
        self.chat_log.insert(tk.END, "Dungeon Master:\n", "bold") # Add "Dungeon Master" in bold
        # self.chat_log.insert(tk.END, f"\tDungeon Master: {reply}\n")
        self.chat_log.insert(tk.END, f"    {reply}\n")
        self.chat_log.insert(tk.END, "\n")  # Add a blank line
        self.chat_log.configure(state="disabled")

    def get_recent_history(self, max_tokens=15000):
        """Return the most recent messages that fit within the token limit."""
        history = []
        token_count = 0 # characters rather than tokens

        for entry in reversed(self.conversation_history):
            # Approximate character count for this entry (can use len or eventually an actual tokenization library)
            entry_tokens = len(entry["user"].split()) + len(entry["response"].split())
            if token_count + entry_tokens > max_tokens:
                break
            history.insert(0, entry)  # Add to the start of the history
            token_count += entry_tokens

        return history


    def send_message(self):
        """Handle sending a message."""
        message = self.chat_input.get().strip()
        if not message:
            return

        # Append message to chat log
        self.chat_log.configure(state="normal")
        # self.chat_log.insert(tk.END, f"You: {message}\n")
        self.chat_log.insert(tk.END, "You:\n", "bold")
        self.chat_log.insert(tk.END, f"    {message}\n")
        self.chat_log.configure(state="disabled")
        self.chat_input.delete(0, tk.END)

        # Prepare the prompt
        prompt = self.prepare_prompt(message)

        # Send the prompt to OpenAI and handle the response
        try:
            response = send_prompt(
                prompt,
                model="gpt-4o",
                max_tokens=16384,
                temperature=0.7,
                role_description="You are an expert dungeon master."
            )
            # Parse and display the response
            # print(response)  # debugging
            self.display_response(response)

            self.conversation_history.append({
                "id": self.message_counter,
                "user": message,
                "response": response.strip()  # After receiving the DM response
            })
            print("message counter: ", self.message_counter)

            # print(self.settings)
            self.save_chat_history(self.chat_file)

            # Increment for next go around
            self.message_counter += 1

        except Exception as e:
            # Handle API errors
            self.chat_log.configure(state="normal")
            self.chat_log.insert(tk.END, f"System: Error fetching response: {e}\n")
            self.chat_log.configure(state="disabled")

    def save_chat_history(self, file_path="chat_history.json"):
        """Save the chat history to a file with checkpoint tracking."""
        try:
            # Check if file exists already
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    existing_data = json.load(f)
                last_saved_index = existing_data.get("last_saved_index", 0)
                saved_history = existing_data.get("conversation_history", [])
            else:
                last_saved_index = 0
                saved_history = []

            # Append only new messages
            new_messages = [
                entry for entry in self.conversation_history
                if entry["id"] > last_saved_index
            ]

            if not new_messages:
                print("No new messages to save.")
                return

            saved_history.extend(new_messages)

            # Update last_saved_index to the highest ID in saved messages
            updated_last_saved_index = max(entry["id"] for entry in saved_history)

            # Update the checkpoint and save the full history
            save_data = {
                "last_saved_index": updated_last_saved_index,
                "conversation_history": saved_history,
            }
            with open(file_path, "w") as f:
                json.dump(save_data, f, indent=4)

            print(f"Chat history saved to {file_path}")
        except Exception as e:
            print(f"Error saving chat history: {e}")


    def load_conversation(self, conversation_history_in):
        """Load a conversation history into the chat log."""
        self.chat_log.configure(state="normal")
        self.chat_log.delete("1.0", tk.END)  # Clear existing chat log

        # Extract the conversation history list
        conversation_history = conversation_history_in.get("conversation_history", [])
        # print(conversation_history)

        for entry in conversation_history:
            if not isinstance(entry, dict):
                print(f"Skipping entry in conversation history: {entry}")
                continue

            try:
                # Display user message
                user_message = entry.get("user", "")
                if user_message:
                    # print("user message: ", user_message)
                    self.chat_log.insert(tk.END, f"Player: {user_message}\n")

                # Display Dungeon Master's response
                dm_response = entry.get("response", "")
                if dm_response:
                    # print("dm response: ", dm_response)
                    self.chat_log.insert(tk.END, f"Dungeon Master:\n    {dm_response}\n")
                    self.chat_log.insert(tk.END, "\n")  # Add a blank line

            except Exception as e:
                print(f"Error parsing conversation entry: {entry}. Error: {e}")

        self.chat_log.configure(state="disabled")
