import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # Speaking speed

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Say it again.")
            return ""
        except sr.WaitTimeoutError:
            speak("No voice detected.")
            return ""

# Weather API
WEATHER_API_KEY = "9f739a2b9af117d2c749ade33b94570b"

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url).json()
        if res.get("main"):
            temp = res['main']['temp']
            desc = res['weather'][0]['description']
            speak(f"The temperature in {city} is {temp}°C with {desc}.")
        else:
            speak("City not found.")
    except:
        speak("Couldn't get weather info. Check your internet.")

# Notes
def remember_note(note):
    with open("notes.txt", "w") as f:
        f.write(note)
    speak("I've noted that.")

def recall_note():
    try:
        with open("notes.txt", "r") as f:
            note = f.read()
            if note:
                speak(f"You asked me to remember: {note}")
            else:
                speak("I don't have anything remembered.")
    except FileNotFoundError:
        speak("No notes found.")

# Website opening
def open_website(site):
    urls = {
        "google meet": "https://meet.google.com",
        "whatsapp web": "https://web.whatsapp.com",
        "chatgpt": "https://chat.openai.com",
        "stackoverflow": "https://stackoverflow.com",
        "linkedin": "https://linkedin.com",
        "instagram": "https://instagram.com",
        "facebook": "https://facebook.com",
        "twitter": "https://twitter.com",
        "netflix": "https://netflix.com",
        "spotify": "https://spotify.com",
        "youtube": "https://youtube.com",
        "github": "https://github.com",
        "gmail": "https://mail.google.com",
        "google": "https://google.com",
        "amazon": "https://amazon.in",
        "flipkart": "https://flipkart.com"
    }
    for key in urls:
        if key in site:
            speak(f"Opening {key}")
            webbrowser.open(urls[key])
            return
    speak("Sorry, I don't know that website.")

# Greeting
def greet():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Hello, I am Jarvis A.I. How can I help you today?")

# Main loop
if __name__ == "__main__":
    greet()
    while True:
        query = take_command()

        if "open" in query:
            open_website(query)

        elif "weather in" in query:
            city = query.split("weather in")[-1].strip()
            get_weather(city)

        elif "remember" in query:
            speak("What should I remember?")
            note = take_command()
            if note:
                remember_note(note)

        elif "do you remember" in query or "what did i ask you to remember" in query:
            recall_note()

        elif "time" in query:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {now}")

        elif "exit" in query or "quit" in query or "stop" in query:
            speak("Goodbye! Have a great day.")
            break

        elif query:
            speak("Sorry, I don't know how to do that yet.")
