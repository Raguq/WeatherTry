import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io

API_KEY = "487edd3533324fa0ace195546240906"
CITIES = ["Tver", "Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg"]

def fetch_weather():
    city = city_var.get()
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=7&aqi=no&alerts=no"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        display_weather(weather_data)
    else:
        error_message = f"Failed to retrieve weather data: {response.status_code} - {response.reason}"
        messagebox.showerror("Error", error_message)

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
        weather_frame.grid(row=i, column=0, pady=5, padx=5)
        
        icon_label = tk.Label(weather_frame)
        icon_label.grid(row=0, column=0, rowspan=2)
        
        temp_label = tk.Label(weather_frame, text=f"{temp_min}°C - {temp_max}°C", font=('Arial', 14))
        temp_label.grid(row=0, column=1, padx=10)
        
        desc_label = tk.Label(weather_frame, text=description.capitalize(), font=('Arial', 12))
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
        if "rain" in description.lower():
            weather_frame.configure(bg="lightblue")
        elif "cloud" in description.lower():
            weather_frame.configure(bg="gray")
        elif "sun" in description.lower() or "clear" in description.lower():
            weather_frame.configure(bg="yellow")
        else:
            weather_frame.configure(bg="white")

root = tk.Tk()
root.title("Weekly Weather Forecast")
root.geometry("500x600")

title_label = tk.Label(root, text="Weekly Weather Forecast", font=('Arial', 20))
title_label.pack(pady=10)

city_var = tk.StringVar(value=CITIES[0])
city_menu = ttk.Combobox(root, textvariable=city_var, values=CITIES, font=('Arial', 14))
city_menu.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

fetch_weather_button = tk.Button(root, text="Fetch Weather", command=fetch_weather, font=('Arial', 14))
fetch_weather_button.pack(pady=10)

root.mainloop()
