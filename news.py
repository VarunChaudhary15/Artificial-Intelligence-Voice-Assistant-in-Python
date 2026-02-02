import requests
import pyttsx3
import speech_recognition as sr

# ------------------ SPEAK FUNCTION ------------------ #
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

# ------------------ LISTEN FUNCTION ------------------ #
def listen(prompt=None, timeout=5, phrase_time_limit=6, retries=2):
    r = sr.Recognizer()
    mic = sr.Microphone()
    for attempt in range(retries):
        if prompt:
            speak(prompt)
        try:
            with mic as source:
                print(f"Listening... (attempt {attempt+1}/{retries})")
                audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = r.recognize_google(audio).lower()
            print("You said:", text)
            return text
        except sr.WaitTimeoutError:
            print("Timeout.")
            continue
        except sr.UnknownValueError:
            print("Could not understand.")
            continue
        except sr.RequestError:
            speak("Internet connection problem.")
            return None
    return None

# ------------------ GET TOP NEWS FUNCTION ------------------ #
def get_top_news(api_key, country="us", num_headlines=3):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'ok':
            articles = data['articles'][:num_headlines]
            return [article['title'] for article in articles]
        else:
            return None
    except:
        return None

# ------------------ MAIN ------------------ #
if __name__ == "__main__":
    API_KEY = "YOUR_NEWSAPI_KEY_HERE"  # Get free API key from https://newsapi.org/

    speak("Hello sir, how can I help you?")
    command = listen(prompt="Please tell me your command")

    if command and "news" in command:
        speak("Fetching the top news headlines for you.")

        headlines = get_top_news(API_KEY, country="us", num_headlines=3)

        if headlines:
            print("\n--- TOP 3 NEWS HEADLINES ---")
            for i, headline in enumerate(headlines, start=1):
                print(f"{i}. {headline}")
                speak(f"Headline {i}: {headline}")
            print("-----------------------------\n")
        else:
            speak("Sorry, I could not fetch news at this moment.")
