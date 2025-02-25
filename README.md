# Language_Translator
# Language Translator Application

## Overview
This Python application is a GUI-based language translator with user authentication. It allows users to register, log in, and translate text between various languages. The application also provides text-to-speech functionality and the ability to copy translated text to the clipboard.

## Features
- **User Authentication**: Users can register and log in using a SQLite database.
- **Language Translation**: Supports multiple languages using Google Translate.
- **Text-to-Speech**: Uses pyttsx3 for speech synthesis.
- **Clipboard Copying**: Easily copy translated text.
- **User-Friendly GUI**: Built with Tkinter for ease of use.

## Prerequisites
Ensure you have the following dependencies installed:

```sh
pip install googletrans==4.0.0-rc1 pyttsx3 bcrypt pillow
```

## Installation
1. Clone this repository or download the source code.
2. Install the required dependencies using the command above.
3. Run the application:

```sh
python main.py
```

## Usage
1. **Launch the Application**: Upon running the script, the login window will appear.
2. **Register a User**: If you are a new user, click "Register" and create an account.
3. **Log In**: Enter your credentials and log in.
4. **Translate Text**:
   - Select the source and target language.
   - Enter the text and click "Translate."
   - Copy or listen to the translated text.
5. **Logout**: Click "Logout" to return to the login screen.

## File Structure
- `main.py`: Main script containing GUI and logic.
- `users.db`: SQLite database storing user credentials.

## Technologies Used
- **Python**
- **Tkinter** (GUI framework)
- **SQLite** (Database for authentication)
- **Googletrans** (Translation API)
- **Pyttsx3** (Text-to-speech engine)

## License
This project is open-source and free to use.

