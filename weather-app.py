# Import required modules
import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap
from ttkbootstrap.constants import *
import geocoder

# Function to get weather information from OpenWeatherMap API
def get_weather(city):
    API_key = "46f85ebae7add0e2f7be9e01b9551c48"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)
    
    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    # Parse the response JSON to get weather information
    weather = res.json()

    #print(weather)

    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    # Additional weather information
    humidity = weather['main']['humidity']
    wind_speed = weather['wind']['speed']
    pressure = weather['main']['pressure']

    # Get the icon URL and return all the weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    
    return (icon_url, temperature, description, city, country, humidity, wind_speed, pressure)

# Function to search weather for a city
def search():
    city = city_entry.get()
    if city == '':
        messagebox.showerror("Error", 'Please enter a city')
        return None
    result = get_weather(city)
    if result is None:
        return
    # If the city is found, unpack the weather information
    icon_url, temperature, description, city, country, humidity, wind_speed, pressure = result
    location_label.configure(text=f"{city}, {country}")

    # Get the weather icon image from the URL and update the icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    # Update the temperature and description labels
    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")
    humidity_label.configure(text=f"Humidity: {humidity}%")
    wind_speed_label.configure(text=f"Wind Speed: {wind_speed} m/s")
    pressure_label.configure(text=f"Pressure: {pressure} hPa")

def search_current_location():
    g = geocoder.ip('me')
    city = g.city
    result = get_weather(city)
    print(result)
    if result is None:
        return
    # If the city is found, unpack the weather information
    icon_url, temperature, description, city, country, humidity, wind_speed, pressure = result
    location_label.configure(text=f"{city}, {country}")

    # Get the weather icon image from the URL and update the icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    # Update the temperature and description labels
    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")
    humidity_label.configure(text=f"Humidity: {humidity}%")
    wind_speed_label.configure(text=f"Wind Speed: {wind_speed} m/s")
    pressure_label.configure(text=f"Pressure: {pressure} hPa")

def change_theme(event):
    t = combo.get()
    style.theme_use(t)

def option_toggle():
    open_stat = False

root = ttkbootstrap.Window(themename = 'solar')
root.title("Weather App")
root.geometry("550x650")
root.minsize(550, 650)
style = root.style

label = ttkbootstrap.Label(root, text = 'Enter a city', font = 'Helvetica, 21')
label.pack(pady=11)

frame = ttkbootstrap.Frame(root)
frame.pack(pady=15)

# Create an entry widget -> to enter the city name
city_entry = ttkbootstrap.Entry(frame, font="Helvetica, 14")
city_entry.pack(side = LEFT, expand = True)

# Create a button widget -> to search for the weather information
search_button = ttkbootstrap.Button(frame, text = '🔎', command=search, bootstyle="primary", padding="20 7.5")
search_button.pack(side = LEFT, padx = 5)

search_current_button = ttkbootstrap.Button(root, text="Get current location instead", command=search_current_location, bootstyle="info-link", width=35)
search_current_button.pack()

# Create a label widget -> to show the city/country name
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack()

# Create a label widget -> to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Create a label widget -> to show the temperature
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

# Create a label widget -> to show the weather description
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

# Create a label widget -> to show the wind speed
wind_speed_label = tk.Label(root, font="Helvetica, 20")
wind_speed_label.pack()

# Create a label widget -> to show the pressure
pressure_label = tk.Label(root, font="Helvetica, 20")
pressure_label.pack()

# Create a label widget -> to show the humidity
humidity_label = tk.Label(root, font="Helvetica, 20")
humidity_label.pack()  

#toggle_button = ttkbootstrap.Button(root, text = 'open-setting(s)')
###############################
change_label = ttkbootstrap.Label(root, text = 'Change theme')
change_label.pack(pady = 5)

combo = ttkbootstrap.Combobox(root, values = ttkbootstrap.Style().theme_names())
combo.pack()
combo.bind('<<ComboboxSelected>>', change_theme)
###############################

root.position_center()
root.mainloop()