import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io

API_KEY = "487edd3533324fa0ace195546240906"
CITIES = ["Тверь", "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург"]

translations = {
    "Weekly Weather Forecast": "Прогноз погоды на неделю",
    "Fetch Weather": "Получить погоду",
    "Failed to retrieve weather data": "Не удалось получить данные о погоде",
    "Error": "Ошибка"
}

weather_translations = {
    "Sunny": "Ясно",
    "Partly cloudy": "Переменная облачность",
    "Cloudy": "Облачно",
    "Overcast": "Пасмурно",
    "Mist": "Туман",
    "Patchy rain possible": "Возможен кратковременный дождь",
    "Patchy snow possible": "Возможен кратковременный снег",
    "Patchy sleet possible": "Возможен кратковременный дождь со снегом",
    "Patchy freezing drizzle possible": "Возможен кратковременный ледяной дождь",
    "Thundery outbreaks possible": "Возможны грозовые вспышки",
    "Blowing snow": "Метель",
    "Blizzard": "Буран",
    "Fog": "Туман",
    "Freezing fog": "Ледяной туман",
    "Patchy light drizzle": "Кратковременный легкий дождь",
    "Light drizzle": "Легкий дождь",
    "Freezing drizzle": "Ледяной дождь",
    "Heavy freezing drizzle": "Сильный ледяной дождь",
    "Patchy light rain": "Кратковременный легкий дождь",
    "Light rain": "Легкий дождь",
    "Moderate rain at times": "Временами умеренный дождь",
    "Moderate rain": "Умеренный дождь",
    "Heavy rain at times": "Временами сильный дождь",
    "Heavy rain": "Сильный дождь",
    "Light freezing rain": "Легкий ледяной дождь",
    "Moderate or heavy freezing rain": "Умеренный или сильный ледяной дождь",
    "Light sleet": "Легкий дождь со снегом",
    "Moderate or heavy sleet": "Умеренный или сильный дождь со снегом",
    "Patchy light snow": "Кратковременный легкий снег",
    "Light snow": "Легкий снег",
    "Patchy moderate snow": "Кратковременный умеренный снег",
    "Moderate snow": "Умеренный снег",
    "Patchy heavy snow": "Кратковременный сильный снег",
    "Heavy snow": "Сильный снег",
    "Ice pellets": "Ледяные гранулы",
    "Light rain shower": "Легкий ливень",
    "Moderate or heavy rain shower": "Умеренный или сильный ливень",
    "Torrential rain shower": "Сильный ливень",
    "Light sleet showers": "Легкий дождь со снегом",
    "Moderate or heavy sleet showers": "Умеренный или сильный дождь со снегом",
    "Light snow showers": "Легкий снегопад",
    "Moderate or heavy snow showers": "Умеренный или сильный снегопад",
    "Light showers of ice pellets": "Легкий дождь с ледяными гранулами",
    "Moderate or heavy showers of ice pellets": "Умеренный или сильный дождь с ледяными гранулами",
    "Patchy light rain with thunder": "Кратковременный легкий дождь с грозой",
    "Moderate or heavy rain with thunder": "Умеренный или сильный дождь с грозой",
    "Patchy light snow with thunder": "Кратковременный легкий снег с грозой",
    "Moderate or heavy snow with thunder": "Умеренный или сильный снег с грозой"
}

def translate(text):
    return translations.get(text, text)

def translate_weather(text):
    return weather_translations.get(text, text)

def fetch_weather():
    city = city_var.get()
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=7&aqi=no&alerts=no"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        display_weather(weather_data)
    else:
        error_message = f"{translate('Failed to retrieve weather data')}: {response.status_code} - {response.reason}"
        messagebox.showerror(translate("Error"), error_message)

def display_weather(weather_data):
    for widget in frame.winfo_children():
        widget.destroy()

    for i, day in enumerate(weather_data['forecast']['forecastday']):
        date = day['date']
        temp_min = day['day']['mintemp_c']
        temp_max = day['day']['maxtemp_c']
        description = day['day']['condition']['text']
        icon = day['day']['condition']['icon']
        
        weather_frame = tk.Frame(frame, bd=2, relief=tk.RAISED, padx=10, pady=10)
        weather_frame.grid(row=i, column=0, pady=5, padx=5, sticky='ew')
        
        icon_label = tk.Label(weather_frame)
        icon_label.grid(row=0, column=0, rowspan=2)
        
        temp_label = tk.Label(weather_frame, text=f"{temp_min}°C - {temp_max}°C", font=('Arial', 14))
        temp_label.grid(row=0, column=1, padx=10)
        
        desc_label = tk.Label(weather_frame, text=translate_weather(description).capitalize(), font=('Arial', 12))
        desc_label.grid(row=1, column=1, padx=10)
        
        # Fetch and display weather icon
        icon_url = f"http:{icon}"
        icon_response = requests.get(icon_url, stream=True)
        if icon_response.status_code == 200:
            icon_data = icon_response.raw.read()
            icon_image = Image.open(io.BytesIO(icon_data))
            icon_image = ImageTk.PhotoImage(icon_image)
            icon_label.configure(image=icon_image)
            icon_label.image = icon_image
        
        # Change background based on weather description
        if "дождь" in description.lower():
            weather_frame.configure(bg="lightblue")
        elif "облачно" in description.lower():
            weather_frame.configure(bg="gray")
        elif "ясно" in description.lower() or "солнечно" in description.lower():
            weather_frame.configure(bg="yellow")
        else:
            weather_frame.configure(bg="white")

root = tk.Tk()
root.title(translate("Weekly Weather Forecast"))

# Allow window resizing
root.geometry("600x700")
root.minsize(500, 600)
root.columnconfigure(0, weight=1)

title_label = tk.Label(root, text=translate("Weekly Weather Forecast"), font=('Arial', 20))
title_label.pack(pady=10)

city_var = tk.StringVar(value=CITIES[0])
city_menu = ttk.Combobox(root, textvariable=city_var, values=CITIES, font=('Arial', 14))
city_menu.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10, fill=tk.BOTH, expand=True)

fetch_weather_button = tk.Button(root, text=translate("Fetch Weather"), command=fetch_weather, font=('Arial', 14))
fetch_weather_button.pack(pady=10)

root.mainloop()
