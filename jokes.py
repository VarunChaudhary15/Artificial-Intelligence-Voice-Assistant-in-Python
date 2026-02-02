import requests
import time

def tell_joke(speak):
    url = "https://official-joke-api.appspot.com/random_joke"

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()

        setup = data.get("setup", "Sorry, I couldn't find a joke.")
        punchline = data.get("punchline", "No punchline available.")

        # Speak both
        speak("Here is a joke sir.")
        speak(setup)
        time.sleep(1)
        speak(punchline)

    except:
        speak("Sorry sir, I could not get any joke right now.")
