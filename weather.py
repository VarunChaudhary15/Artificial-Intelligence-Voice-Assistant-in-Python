import requests

# Your API key
API_KEY = "063e799ba7c8d92eb4a35d0f4ef819ad"

# City you want to check
CITY = "Jaipur"

# API URL
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# ---- Fetch JSON ---- #
response = requests.get(URL)
json_data = response.json()

print("API Response:", json_data)   # Debugging output

# ---- Temperature Function ---- #
def temp():
    try:
        temperature = round(json_data["main"]["temp"])
        return temperature
    except:
        return "Temperature not available"

# ---- Weather Description Function ---- #
def description():
    try:
        desc = json_data["weather"][0]["description"]
        return desc
    except:
        return "Description not available"

# ---- OUTPUT ---- #
print("\n--- WEATHER REPORT ---")
print("City:", CITY)
print("Temperature:", temp(), "°C")
print("Weather:", description())
