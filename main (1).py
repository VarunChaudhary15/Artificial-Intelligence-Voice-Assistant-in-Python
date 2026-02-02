import speech_recognition as sr
import pyttsx3
import time
import webbrowser
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import randfacts
import requests
# -------------------------------------------------------------------
# SPEAK FUNCTION
# -------------------------------------------------------------------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')

    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)

    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# -------------------------------------------------------------------
# LISTEN
# -------------------------------------------------------------------
STOP_WORDS = ["stop", "bye", "exit", "quit", "thank you", "that's all"]
INFO_WORDS = ["information", "in formation", "info", "about", "search", "wikipedia"]
FACT_WORDS = ["fact", "random fact", "tell me something", "fun fact", "something new"]
WEATHER_WORDS = ["temperature", "weather", "climate", "temprature", "temprature today"]

r = sr.Recognizer()
mic = sr.Microphone()

def listen(prompt=None, timeout=5, phrase_time_limit=6, retries=2):
    for _ in range(retries):
        if prompt:
            speak(prompt)

        try:
            with mic as source:
                print("Listening...")
                audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

            text = r.recognize_google(audio).lower()
            print("Heard:", text)
            return text

        except:
            print("Could not understand.")
            continue

    return None


# -------------------------------------------------------------------
# WEATHER FEATURE (JAIPUR)
# -------------------------------------------------------------------
API_KEY = "063e799ba7c8d92eb4a35d0f4ef819ad"
CITY = "Jaipur"

def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return None, None

        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]

        return temperature, description

    except:
        return None, None


# -------------------------------------------------------------------
# YOUTUBE
# -------------------------------------------------------------------
def play_youtube(query, play_duration=120):
    speak(f"Searching {query} on YouTube")

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 15)
    driver.get("https://www.youtube.com")
    time.sleep(2)

    # Accept consent
    try:
        consent = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//tp-yt-paper-button[contains(text(),"I agree")]')
        ))
        consent.click()
    except:
        pass

    search_box = wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
    search_box.send_keys(query)
    search_box.send_keys(Keys.ENTER)

    video = wait.until(EC.element_to_be_clickable((By.ID, "video-title")))
    video.click()

    speak("Playing now.")
    time.sleep(play_duration)
    driver.quit()


# -------------------------------------------------------------------
# JOKE
# -------------------------------------------------------------------
def tell_joke():
    try:
        res = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke = res.json()

        speak("Here is a joke sir.")
        speak(joke["setup"])
        time.sleep(1)
        speak(joke["punchline"])
    except:
        speak("Sorry sir, I could not load a joke.")


# -------------------------------------------------------------------
# FACT
# -------------------------------------------------------------------
def tell_fact():
    try:
        fact = randfacts.get_fact()
        speak("Here is a random fact sir.")
        speak(fact)
    except:
        speak("Sorry sir, I could not get a fact.")


# -------------------------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------------------------
with mic as source:
    print("Calibrating noise...")
    r.adjust_for_ambient_noise(source, duration=1.2)
    print("Ready.")

speak("Hello sir, I'm your voice assistant. How are you?")

while True:
    reply = listen(timeout=5, phrase_time_limit=5, retries=2)

    if reply is None:
        speak("Sorry sir, I didn't catch that. How are you?")
        continue

    if any(w in reply for w in STOP_WORDS):
        speak("Okay sir, stopping now. Have a great day!")
        break

    if "fine" in reply or "good" in reply:
        speak("I am having a good day sir.")
    else:
        speak("Okay sir.")

    command = listen("What can I do for you?", timeout=6, phrase_time_limit=7, retries=2)

    if command is None:
        speak("I did not hear any command. Let's try again.")
        continue

    if any(w in command for w in STOP_WORDS):
        speak("Alright sir, shutting down. Goodbye!")
        break

    # TEMPERATURE FEATURE
    if any(w in command for w in WEATHER_WORDS):
        temp, desc = get_weather()

        if temp is None:
            speak("Sorry sir, I could not fetch the weather.")
        else:
            speak(f"Sir, the current temperature in Jaipur is {temp} degrees Celsius.")
            speak(f"The weather is {desc}.")
        continue

    # JOKE FEATURE
    if "joke" in command or "funny" in command:
        tell_joke()
        continue

    # FACT FEATURE
    if any(w in command for w in FACT_WORDS):
        tell_fact()
        continue

    # INFORMATION FEATURE
    if any(word in command for word in INFO_WORDS):
        topic = listen("Which topic sir?", timeout=8, phrase_time_limit=10, retries=3)

        if topic:
            speak(f"Opening Wikipedia for {topic}")
            url = "https://en.wikipedia.org/wiki/" + quote(topic.replace(" ", "_"))
            webbrowser.open(url)
        else:
            speak("I couldn't get the topic sir.")
        continue

    # YOUTUBE FEATURE
    play_youtube(command, play_duration=120)
