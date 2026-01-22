# 📖 The Infinite Muse

*A creative writing assistant with personality*

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 🎭 **The Muse's Personality**
- Speaks in poetic, mysterious metaphors
- Provides symbolic analysis of prompts  
- Maintains consistent creative voice
- Responds differently based on your mood

### 📖 **Smart Prompt Generation**
- Random character + setting + conflict combinations
- Genre-specific prompts (mystery, fantasy, sci-fi, horror, noir)
- Plot twist suggestions
- Writing tips and inspiration

### 💾 **Data Management**
- Save favorites locally in JSON format
- Export prompts as text or JSON files
- Persistent storage between sessions
- Remove unwanted prompts

## 🚀 Quick Start

### Installation
```bash
cd prompt_generator
pip install -r requirements.txt
streamlit run app.py

Basic Usage
Open http://localhost:8501

Select a genre from sidebar

Click "Generate" or type "give me a prompt"

Use buttons to save, add twists, or get explanations

📁 Project Structure
prompt_generator/
├── app.py              # Main Streamlit app
├── muse_bot.py         # Chatbot class
├── chatbot_base.py     # Base class
├── requirements.txt    # Dependencies
├── utils/
│   └── data_manager.py # File handling
└── data/
    └── favorites.json  # Saved prompts

🎯 Key Commands
"prompt" - Generate story idea

"twist" - Add plot twist

"explain" - Get symbolic analysis

"save" - Save to favorites

"clear" - Reset conversation

"help" - Show all commands

🔧 Requirements
Python 3.8+

Streamlit 1.28+

No external APIs needed

📝 License
MIT License - Free for personal and educational use

🤝 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a Pull Request

