import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

def get_weather(city):
    if not API_KEY:
        return None, "OpenWeather API key is missing. Add it to your environment."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 404:
            return None, "City not found."
        response.raise_for_status()
        data = response.json()

        weather = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind": round(data["wind"].get("speed", 0), 1),
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "visibility": round(data.get("visibility", 0) / 1000, 1),
        }
        return weather, None
    except requests.RequestException:
        return None, "Weather service is unavailable. Try again."

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            error = "Enter a city name."
        else:
            weather, error = get_weather(city)

    return render_template("index.html", weather=weather, error=error, city=city)

if __name__ == "__main__":
    app.run(debug=True)
