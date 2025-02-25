import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
import pyttsx3
import sqlite3
import bcrypt
from PIL import Image, ImageTk  # For Background Image

# Database Setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")
conn.commit()

# Initialize Translator and TTS Engine
translator = Translator()
tts_engine = pyttsx3.init()

class LanguageTranslator:
    def __init__(self, root, username):
        self.root = root
        self.root.title(f"Language Translator - Welcome, {username}")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # Set Background Color
        self.root.configure(bg="#ecf0f1")

        # Header Frame
        header_frame = tk.Frame(root, bg="#2c3e50")
        header_frame.place(relwidth=1, height=50)

        # Header Label
        tk.Label(header_frame, text=f"Welcome, {username}", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=10)

        # Main Content Frame (to avoid overlap with the header)
        content_frame = tk.Frame(root, bg="#ecf0f1")
        content_frame.place(relwidth=1, rely=0.1, relheight=0.9)

        # Language selection dropdowns
        self.languages = list(LANGUAGES.values())

        tk.Label(content_frame, text="Source Language:", bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.source_language = ttk.Combobox(content_frame, values=self.languages, state="readonly", font=("Arial", 10))
        self.source_language.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.source_language.set("english")

        tk.Label(content_frame, text="Target Language:", bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.target_language = ttk.Combobox(content_frame, values=self.languages, state="readonly", font=("Arial", 10))
        self.target_language.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.target_language.set("spanish")

        # Input text area
        tk.Label(content_frame, text="Enter Text:", bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.input_text = tk.Text(content_frame, height=10, width=40, font=("Arial", 12), bg="white", fg="#2c3e50")
        self.input_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Output text area
        tk.Label(content_frame, text="Translated Text:", bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12)).grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.output_text = tk.Text(content_frame, height=10, width=40, font=("Arial", 12), bg="white", fg="#2c3e50", state="disabled")
        self.output_text.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

        # Buttons
        button_frame = tk.Frame(content_frame, bg="#ecf0f1")
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)

        tk.Button(button_frame, text="Translate", command=self.translate_text, font=("Arial", 12, "bold"), bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Copy Text", command=self.copy_to_clipboard, font=("Arial", 12, "bold"), bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Speak Text", command=self.speak_translated_text, font=("Arial", 12, "bold"), bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Logout", command=self.logout, font=("Arial", 12, "bold"), bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=5)
    
    def translate_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return

        source_lang = self.source_language.get()
        target_lang = self.target_language.get()

        try:
            translated = translator.translate(text, src=source_lang, dest=target_lang)
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated.text)
            self.output_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Translation Error", f"An error occurred: {e}")

    def copy_to_clipboard(self):
        translated_text = self.output_text.get("1.0", tk.END).strip()
        if translated_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(translated_text)
            messagebox.showinfo("Copied", "Translated text copied to clipboard!")

    def speak_translated_text(self):
        translated_text = self.output_text.get("1.0", tk.END).strip()
        if translated_text:
            tts_engine.say(translated_text)
            tts_engine.runAndWait()

    def logout(self):
        self.root.destroy()
        show_login()

# Authentication Functions (unchanged)
def register_user():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful! Please log in.")
        register_window.destroy()
        show_login()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

def login_user():
    username = username_entry.get()
    password = password_entry.get()

    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()

    if result and bcrypt.checkpw(password.encode(), result[0]):
        messagebox.showinfo("Success", "Login successful!")
        login_window.destroy()
        show_translator(username)
    else:
        messagebox.showerror("Error", "Invalid username or password!")

# GUI for Login & Register (unchanged)
def show_login():
    global login_window, username_entry, password_entry
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x250")
    login_window.configure(bg="#ecf0f1")

    tk.Label(login_window, text="Username:", bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12)).pack()
    username_entry = tk.Entry(login_window, font=("Arial", 12))
    username_entry.pack()

    tk.Label(login_window, text="Password:", bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12)).pack()
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
    password_entry.pack()

    tk.Button(login_window, text="Login", command=login_user, font=("Arial", 12, "bold"), bg="#3498db", fg="white").pack(pady=10)
    tk.Button(login_window, text="Register", command=show_register, font=("Arial", 12, "bold"), bg="#2c3e50", fg="white").pack(pady=5)

    login_window.mainloop()

def show_register():
    global register_window, username_entry, password_entry
    register_window = tk.Tk()
    register_window.title("Register")
    register_window.geometry("300x250")
    register_window.configure(bg="#ecf0f1")

    tk.Label(register_window, text="Username:", bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12)).pack()
    username_entry = tk.Entry(register_window, font=("Arial", 12))
    username_entry.pack()

    tk.Label(register_window, text="Password:", bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12)).pack()
    password_entry = tk.Entry(register_window, show="*", font=("Arial", 12))
    password_entry.pack()

    tk.Button(register_window, text="Register", command=register_user, font=("Arial", 12, "bold"), bg="#3498db", fg="white").pack(pady=10)

def show_translator(username):
    root = tk.Tk()
    app = LanguageTranslator(root, username)
    root.mainloop()

if __name__ == "__main__":
    show_login()