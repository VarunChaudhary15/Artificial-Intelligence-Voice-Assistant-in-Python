from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import speech_recognition as sr
import pyttsx3
import time


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()


class YoutubePlayer:
    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 15)

    def play_first_video(self, query):
        speak(f"Searching {query} on YouTube")
        self.driver.get("https://www.youtube.com")
        time.sleep(2)

        # Accept cookies if shown
        try:
            consent_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//tp-yt-paper-button[contains(text(),"I agree")]'))
            )
            consent_button.click()
            time.sleep(1)
        except:
            pass

        # Search query
        search_box = self.wait.until(
            EC.presence_of_element_located((By.NAME, "search_query"))
        )
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)

        # Click first video
        first_video = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[@id="video-title"]'))
        )
        first_video.click()

        # Wait for the video element
        video = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )

        # Force play
        self.driver.execute_script("arguments[0].play();", video)
        speak("Playing now. Enjoy!")

        # Wait for 2 minutes (120 seconds)
        time.sleep(120)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("What should I search on YouTube?")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="en-in")
        print("You said:", text)
        return text
    except:
        speak("I did not understand. Please say it again.")
        return ""


# MAIN
if __name__ == "__main__":
    query = take_command()
    if query:
        yt = YoutubePlayer()
        yt.play_first_video(query)
