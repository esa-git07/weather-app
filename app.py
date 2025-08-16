from flask import Flask, render_template, request
import requests

app = Flask(__name__)

import os
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return render_template("result.html", city=city, error="City not found", temp=None)

    temp = data['main']['temp']
    weather_desc = data['weather'][0]['description']
    icon = data['weather'][0]['icon']

    
    # Clothing suggestion
    if temp < 15:
        clothing = "It’s giving ❄️ Elsa vibes. Layer up bestie, wear a warm jacket and maybe a scarf."
    elif 15 <= temp <= 25:
        clothing = "Perfect weather for a ✨photo dump✨,Jeans + tee kinda day."
    else:
        clothing = "Too hot to care,T-shirt and sunglasses are perfect."

# Gradient based on weather condition
    if "clear" in weather_desc.lower():
     gradient = "linear-gradient(to right, #f9d423, #ff4e50)"  # sunny
    elif "cloud" in weather_desc.lower():
     gradient = "linear-gradient(to right, #bdc3c7, #2c3e50)"  # cloudy gray
    elif "rain" in weather_desc.lower() or "drizzle" in weather_desc.lower():
     gradient = "linear-gradient(to right, #4b79a1, #283e51)"  # rainy blue
    elif "snow" in weather_desc.lower():
     gradient = "linear-gradient(to right, #83a4d4, #b6fbff)"  # snowy icy
    elif "mist" in weather_desc.lower() or "fog" in weather_desc.lower() or "haze" in weather_desc.lower():
     gradient = "linear-gradient(to right, #757f9a, #d7dde8)"  # misty gray
    else:
     gradient = "linear-gradient(to right, #667db6, #0082c8, #0082c8, #667db6)"  # fallback

    return render_template(
        'result.html',
        city=city,
        temp=temp,
        weather=weather_desc.title(),
        icon=icon,
        gradient=gradient,
        clothing=clothing,
        error=None
    )

if __name__ == '__main__':
    app.run(debug=True)
