import datetime
import speech_recognition as sr
import wikipedia
import os
import webbrowser
import pyjokes
import pywhatkit as kit
import tempfile
import playsound
from gtts import gTTS
import tkinter as tk
from tkinter import ttk, LEFT, BOTH, SUNKEN
from PIL import Image, ImageTk
from threading import Thread

# Constants for custom styling
BG_COLOR = "#2E2E2E"  # Dark gray background
BUTTON_COLOR = "#4CAF50"  # Green button color
BUTTON_FONT = ("Arial", 14, "bold")
BUTTON_FOREGROUND = "white"  # White text on buttons
HEADING_FONT = ("white", 24, "bold")  # White heading text
INSTRUCTION_FONT = ("Helvetica", 14, "lightgray")  # Light gray instruction text

# Global variables
entry = None
stop_flag = False

def speak(audio):
    """Convert text to speech."""
    with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
        tts = gTTS(text=audio, lang='en')
        tts.save(f"{tmp_file.name}.mp3")
        playsound.playsound(f"{tmp_file.name}.mp3")

def wish_time():
    """Greet the user based on the current time."""
    name = entry.get() or "User  "
    hour = datetime.datetime.now().hour
    greetings = [
        ("Good night! Sleep tight.", hour < 6),
        ("Good morning!", hour < 12),
        ("Good afternoon!", hour < 18),
        ("Good evening!", True)
    ]
    for greeting, condition in greetings:
        if condition:
            speak(greeting)
            break
    speak(f"{name}, how can I help you?")

def take_command():
    """Listen for a command and return it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        return recognizer.recognize_google(audio, language='en-in')
    except (sr.UnknownValueError, sr.RequestError):
        print("Could not understand audio.")
        return None

def perform_task():
    """Perform tasks based on the recognized command."""
    global stop_flag
    while not stop_flag:
        query = take_command()
        if query:
            query = query.lower()
            if 'wikipedia' in query:
                search_wikipedia(query)
            elif 'play' in query:
                play_song(query)
            elif 'open youtube' in query:
                webbrowser.open("https://www.youtube.com/")
            elif 'open google' in query:
                webbrowser.open("https://www.google.com/")
            elif 'search' in query:
                search_google(query)
            elif 'the time' in query:
                tell_time()
            elif 'open code' in query:
                open_code_editor()
            elif 'joke' in query:
                tell_joke()
            elif "where is" in query:
                locate_place(query)
            elif 'exit' in query:
                stop_voice_assistant()

def search_wikipedia(query):
    """Search Wikipedia for a given query."""
    speak('Searching Wikipedia...')
    query = query.replace("wikipedia", "").strip()
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    except Exception:
        speak("I couldn't find any results.")

def play_song(query):
    """Play a song on YouTube."""
    song = query.replace('play', "").strip()
    speak(f"Playing {song}")
    kit.playonyt(song)

def search_google(query):
    """Search Google for a given query."""
    search_query = query.replace('search', '').strip()
    kit.search(search_query)

def tell_time():
    """Tell the current time."""
    str_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {str_time}")

def open_code_editor():
    """Open the code editor."""
    code_path = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
    os.startfile(code_path)

def tell_joke():
    """Tell a random joke."""
    speak(pyjokes.get_joke())

def locate_place(query):
    """Open Google Maps to locate a place."""
    location = query.replace("where is", "").strip()
    speak(f"Locating {location}")
    webbrowser.open(f"https://www.google.nl/maps/place/{location.replace(' ', '+')}")

def stop_voice_assistant():
    """Stop the voice assistant."""
    global stop_flag
    speak("Stopping the Voice Assistant.")
    stop_flag = True

def start_voice_assistant():
    """Start the voice assistant."""
    global stop_flag
    wish_time()
    perform_task()
    stop_flag = False  # Reset the flag to False when starting the voice assistant

def main():
    """Create and run the main GUI for the voice assistant."""
    global entry
    root = tk.Tk()
    root.title("Voice Assistant")
    root.geometry("500x650")
    root.configure(bg=BG_COLOR)

    def on_button_click():
        """Handle button click to start or stop the voice assistant."""
        global stop_flag
        if not stop_flag:
            Thread(target=start_voice_assistant).start()
        else:
            stop_voice_assistant()

    # Load and set the background image
    background_image = Image.open("D:\\projects\\Vocie_assistant\\wallpaperflare.com_wallpaper.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = ttk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    f1 = ttk.Frame(root)
    f1.pack(pady=100)

    image2 = Image.open("D:\\projects\\Vocie_assistant\\mic.jpg")
    resized_image = image2.resize((120, 120))
    p2 = ImageTk.PhotoImage(resized_image)
    l2 = ttk.Label(f1, image=p2, relief=SUNKEN)
    l2.pack(side="top", fill="both")

    # Heading
    heading_label = ttk.Label(root, text="Voice Assistant", font=HEADING_FONT, background=BG_COLOR)
    heading_label.pack(pady=20)

    f1 = ttk.Frame(root)
    f1.pack()
    l1 = ttk.Label(f1, text="Enter Your Name", font=INSTRUCTION_FONT, background=BG_COLOR)
    l1.pack(side=LEFT, fill=BOTH)
    entry = ttk.Entry(f1, width=30)
    entry.pack(pady=10)

    # Instruction
    instruction_label = ttk.Label(root, text="Click the button below to start the Voice Assistant.",
                                   font=INSTRUCTION_FONT, background=BG_COLOR)
    instruction_label.pack(pady=10)

    # Create and place a button on the GUI
    button = ttk.Button(root, text="Start Voice Assistant", command=on_button_click,
                        style="VoiceAssistant.TButton")
    button.pack(pady=20)

    # Style the button
    style = ttk.Style(root)
    style.configure("VoiceAssistant.TButton", font=BUTTON_FONT, background=BUTTON_COLOR, foreground=BUTTON_FOREGROUND)

    # Run the GUI main loop
    root.mainloop()

if __name__ == "__main__":
    main()