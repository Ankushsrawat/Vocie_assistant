# Assistant
*This Python Voice Assistant with GUI is a user-friendly application designed to interact with users using voice commands and provides a graphical user interface (GUI) for easy control. The assistant is capable of performing various tasks based on user input.*

This Python Voice Assistant with GUI uses Tkinter to enable users to interact through voice commands. It performs tasks like Wikipedia searches,google searches, YouTube music playback, website opening, providing a fun and interactive voice-based experience.



*Features:*
-------------------
**Speech Recognition: Utilizes the speech_recognition module to recognize user's speech through the microphone, enabling seamless communication with the assistant.**

**Text-to-Speech: Implements pyttsx3 to convert the assistant's responses into speech, allowing it to interact audibly with the user.**

**Wikipedia Search: Enables users to query information from Wikipedia by using the wikipedia module to access relevant summaries.**

**YouTube Music Player: Allows users to play their favorite songs on YouTube by utilizing the pywhatkit module to search and play music videos.**

**Web Browsing: Provides convenient access to YouTube and Google using the webbrowser module, allowing users to open these sites quickly.**

**Joke Generator: Amuses users with jokes retrieved from the pyjokes module.**

**Current Time Display: Informs users of the current time through voice feedback using the datetime module.**

**Location Search: Assists users in locating places through Google Maps with the help of the webbrowser module.**

**User Interaction: The assistant prompts users to enter their names and greets them accordingly, creating a personalized experience.**

*Instructions for GUI:*
-------------------------------
**Click the "Start Voice Assistant" button to initiate the assistant's operation.**

**Once started, users can communicate with the assistant using voice commands.**

**Saying "exit" stops the assistant and displays a gratitude message.**

**Users can restart the assistant by clicking the button again.**

Modules Used:
------------------
pyttsx3: For converting text to speech.

datetime: For handling date and time-related functions.

speech_recognition (sr): For recognizing speech from the microphone.

wikipedia: To access information from Wikipedia.

os: For starting applications on the system.

webbrowser: For opening websites in the default web browser.

pyjokes: To generate random jokes for entertainment.

pywhatkit (kit): For playing songs on YouTube and performing web searches.

time: For handling time-related operations.

plyer.notification: For showing notifications.


Modules to Install:
-----------------------------
pyttsx3: pip install pyttsx3

speech_recognition: pip install SpeechRecognition

wikipedia: pip install wikipedia-api

pywhatkit: pip install pywhatkit

plyer: pip install plyer

tkinter: Pre-installed with Python (no need for separate installation).

PIL (Pillow): pip install pillow (for handling images).


This project offers an engaging and functional voice assistant with a GUI, providing a user-friendly interface for various tasks and enjoyable interactions.

*This project is continuously evolving, and more features will be added over time. You can also contribute to the project by adding your own unique features and enhancements. Future planned features include email sending, reminders, calendar events, and more. If you have any new ideas or want to collaborate on enhancing the Voice Assistant's functionality, feel free to create pull requests or open issues on the repository. Contributions from the open-source community are warmly welcomed!*

*code*
--------------
# Import necessary libraries
import datetime
import speech_recognition as sr
import wikipedia
import os
import webbrowser
import pyjokes 
import pywhatkit as kit
import time
import dateparser  
from plyer import notification
import tkinter as tk
from tkinter import ttk
from tkinter import LEFT, BOTH, SUNKEN
from PIL import Image, ImageTk
from threading import Thread
from gtts import gTTS
import playsound
import tempfile

# Constants for custom styling
BG_COLOR = "#2E2E2E"  # Dark gray background
BUTTON_COLOR = "#4CAF50"  # Green button color
BUTTON_FONT = ("Arial", 14, "bold")
BUTTON_FOREGROUND = "white"  # White text on buttons
HEADING_FONT = ("white", 24, "bold")  # White heading text
INSTRUCTION_FONT = ("Helvetica", 14)  # Only specify font family and size

def speak(audio):
    """Convert text to speech using gTTS."""
    with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
        tts = gTTS(text=audio, lang='en')
        tts.save(f"{tmp_file.name}.mp3")
        playsound.playsound(f"{tmp_file.name}.mp3")

entry = None
stop_flag = False

def wish_time():
    global entry
    x = entry.get() or "User   "
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 6:
        speak('Good night! Sleep tight.')
    elif 6 <= hour < 12:
        speak('Good morning!')
    elif 12 <= hour < 18:
        speak('Good afternoon!')
    else:
        speak('Good evening!')
    speak(f"{x}, how can I help you?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        speak("Say something")
        recognizer.pause_threshold = 0.8
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        speak("Recognizing")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def set_alarm(alarm_time):
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            speak("Alarm! It's time!")
            break
        time.sleep(30)

def start_alarm(alarm_time):
    speak(f"Alarm set for {alarm_time}.")
    Thread(target=set_alarm, args=(alarm_time,)).start()

def perform_task():
    global stop_flag
    while not stop_flag:
        query = take_command().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError:
                speak(f"There are multiple meanings for '{query}'. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak(f"'{query}' does not match any Wikipedia page. Please try again.")
        elif 'play' in query:
            song = query.replace('play', "")
            speak("Playing " + song)
            kit.playonyt(song)
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com/")
        elif 'open google' in query:
            webbrowser.open("https://www.google.com/")
        elif 'search' in query:
            s = query.replace('search', '')
            kit.search(s)
        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {str_time}")
        elif 'open code' in query:
            code_path = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(code_path)
        elif 'joke' in query:
            speak(pyjokes.get_joke())
        elif 'set an alarm for' in query:
            try:
                alarm_time = query.split("set an alarm for")[-1].strip()
                parsed_time = dateparser.parse(alarm_time)
                if parsed_time:
                    formatted_time = parsed_time.strftime("%H:%M")
                    start_alarm(formatted_time)
                else:
                    speak("I couldn't understand the time. Please specify it clearly.")
            except Exception as e:
                speak("I couldn't understand the time. Please specify it clearly.")
        elif 'open ai' in query:
            webbrowser.open("https://www.blackbox.ai/")
            speak("Opening OpenAI ")
        elif 'exit' in query:
            speak("Thanks for giving your time.")
            stop_voice_assistant()

def stop_voice_assistant():
    global stop_flag
    speak("Stopping the Voice Assistant.")
    stop_flag = True

def start_voice_assistant():
    global stop_flag
    wish_time()
    perform_task()
    stop_flag = False

def main():
    root = tk.Tk()
    root.title("Voice Assistant")
    root.geometry("500x650")
    root.configure(bg=BG_COLOR)

    def on_button_click():
        global stop_flag
        if not stop_flag:
            stop_flag = False
            Thread(target=start_voice_assistant).start()
        else:
            stop_voice_assistant()

    background_image = Image.open("C:\\projects\\Vocie_assistant\\wallpaperflare.com_wallpaper.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = ttk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    f1 = ttk.Frame(root)
    f1.pack(pady=100)

    image2 = Image.open("C:\\projects\\Vocie_assistant\\mic.jpg")
    resized_image = image2.resize((120, 120))
    p2 = ImageTk.PhotoImage(resized_image)
    l2 = ttk.Label(f1, image=p2, relief=SUNKEN)
    l2.pack(side="top", fill="both")

    heading_label = ttk.Label(root, text="Voice Assistant", font=HEADING_FONT, background=BG_COLOR)
    heading_label.pack(pady=20)

    global entry
    f1 = ttk.Frame(root)
    f1.pack()
    l1 = ttk.Label(f1, text="Enter Your Name", font=INSTRUCTION_FONT, background=BG_COLOR, foreground="lightgray")
    l1.pack(side=LEFT, fill=BOTH)
    entry = ttk.Entry(f1, width=30)
    entry.pack(pady=10)

    instruction_label = ttk.Label(root, text="Click the button below to start the Voice Assistant.", font=INSTRUCTION_FONT, background=BG_COLOR)
    instruction_label.pack(pady=10)

    button = ttk.Button(root, text="Start Voice Assistant", command=on_button_click, style="VoiceAssistant.TButton")
    button.pack(pady=20)

    style = ttk.Style(root)
    style.configure("VoiceAssistant.TButton", font=BUTTON_FONT, background=BUTTON_COLOR, foreground=BUTTON_FOREGROUND)

    root.mainloop()

if __name__ == "__main__":
    main()