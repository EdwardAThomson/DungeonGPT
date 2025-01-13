# DungeonGPT
## Description

DungeonGPT is an interactive, AI-powered Dungeon Master tool designed to guide players through customized adventures in a tabletop role-playing game. The application features dynamic character creation, party selection, game settings customization, and conversational gameplay, all powered by GPT4o.

**OpenAI API key required.**

![DungeonGPT - a lone figure roams through the forest](./pictures/through_the_forest.webp)

## Features

### 🎮 Game Flow
- **Start Game**: Choose between creating a new game or loading an existing one.
- **Character Creation**: Design custom characters with various attributes, classes, and races.
- **Party Selection**: Build your adventuring party from saved characters.
- **Game Settings**: Customize game settings like difficulty, narrative style, and interaction levels.
- **Chat Interface**: Engage in real-time, immersive conversations with the Dungeon Master AI.

### 💾 Save and Load
- Save game settings, party members, and chat histories.
- Load saved games to continue your adventure seamlessly.

### 🔗 Integration with AI
- Powered by OpenAI GPT4o to deliver compelling, interactive narratives.
- Maintains session history for coherent storytelling.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/EdwardAThomson/dungeongpt.git
   cd dungeongpt
   ```
   
2. **Install Dependencies** (Make sure you have Python installed):
   ```bash
    pip install Pillow python-dotenv openai
   ```

3. **Run the Application**
    ```bash
    python main.py
    ```


## Configuration

* **OpenAI API Key:** To use the GPT-powered AI, you need an OpenAI API key. Set your key as an environment variable:

    ```bash
    echo "OPENAI_API_KEY=your-api-key" > .env
    ```

Replace your-api-key with your actual OpenAI API key.