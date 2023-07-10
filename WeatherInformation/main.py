import tkinter as tk
import requests
from tkinter import *
from PIL import ImageTk,Image
from datetime import datetime
import os
import locale
locale.setlocale(locale.LC_ALL,'tr_TR.UTF-8')
# Can Çalışkan - 20200601018
# Bedirhan Asar - 20200601009
# Hasan Baran Arıkan - 20200601007


SETTINGS_FILE = "Settings.txt"
DEFAULT_CITY = ""
DEFAULT_TEMP_UNIT = "Celsius"

city = ""
temp = -273
feels_temp = ""
humidity = ""
icon = ""
condition = ""
sunrise = ""
sunset = ""
condition_string=''

url = "https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid"
api_key = "ce986b6d788bfb91d9d55b2c31b81768"
iconUrl = "http://openweathermap.org/img/wn/{}@2x.png"

dropdownlist_options_list=["Adana","Ankara","Antalya","İstanbul","İzmir","Tunceli","Rize","Malatya","Mersin","Hatay"]
dropdownlist_options_list=sorted(dropdownlist_options_list,key=locale.strxfrm)
parameters=[]
is_celcious = True
is_dropdown_used=False



def getWather(city_input):
    params = {"q": city_input, "appid": api_key, "lang": "eng"}
    data = requests.get(url, params=params).json()
    global city, temp, feels_temp, humidity, icon, condition, sunrise, sunset
    if data:
        city = data["name"].capitalize()
        temp = int(data["main"]["temp"] - 273.15)
        feels_temp = int(data["main"]["feels_like"] - 273.15)
        humidity = int(data["main"]["humidity"])
        icon = data["weather"][0]["icon"]
        condition = data["weather"][0]["description"].capitalize()
        sunrise = int(data["sys"]["sunrise"])
        sunset = int(data["sys"]["sunset"])
        wind_speed = int(data["wind"]["speed"])
        return (city, temp, feels_temp, humidity, icon, condition, sunrise, sunset,wind_speed)

def save_preferences(city, temp):
    with open(SETTINGS_FILE, "w") as file:
        file.write(f"City: {city}\n")
        file.write(f"Temperature Unit: {temp} \n")
        file.write(f"Temperature isC: {is_celcious}")


        main_screen.destroy()
def save_preferences_subMethod():
    save_preferences(city,temp)

def load_preferences():
    global city,temp,is_celcious
    if os.path.exists('Settings.txt'):
        with open(SETTINGS_FILE, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("City:"):
                    city = line.split(":")[1].strip()
                    city_temp_list=city.split()
                    if(len(city_temp_list)==0):
                        city=DEFAULT_CITY
                        main_screen_textBox.insert("1.0", " City: " + city + "\n")
                    else:
                        city = city_temp_list[0]
                        main_screen_textBox.insert("1.0", " City: " + city + "\n")
                    clicked.set(city)
                elif line.startswith("Temperature Unit:"):
                    temp = line.split(":")[1].strip()
                    temp=temp
                    main_screen_textBox.insert("2.0", " Temperature: " + str(temp) + "\n")
                elif line.startswith("Temperature isC:"):
                    temp_isCelcius = line.split(":")[1].strip()
                    if temp_isCelcius !='True':
                        is_celcious=False;
                        C_F_button.config(text='Fahrenheit')

            return city, temp
    else:
        return DEFAULT_CITY, DEFAULT_TEMP_UNIT

def dropdown_clicked(input_in):
    global is_celcious, temp, is_dropdown_used,feels_temp
    is_dropdown_used=True
    global parameters
    main_screen_textBox.delete('1.0','end')
    parameters=list(getWather(input_in))
    city_temp_list=parameters[0].split()
    city_temp_string=city_temp_list[0]
    parameters[0]=""
    parameters[0]=city_temp_string
    main_screen_textBox.insert(tk.END, " City: " + parameters[0] + '\n')
    if(is_celcious!=True):
        temp_temp=parameters[1]
        temp = float((temp_temp * 9 / 5) + 32)
        main_screen_textBox.insert(tk.END, " Temperature: " + str(temp) + "°F" + '\n')
    else:
        main_screen_textBox.insert(tk.END, " Temperature: " + str(parameters[1]) + "°C" + '\n')
        temp=parameters[1]

    if (is_celcious != True):
        temp_tempfelt = parameters[2]
        feels_temp = float((temp_tempfelt * 9 / 5) + 32)
        main_screen_textBox.insert(tk.END, " Temperature felt: " + str(feels_temp) + "°F" + '\n')
    else:
        main_screen_textBox.insert(tk.END, " Temperature felt: " + str(parameters[2]) + "°C" + '\n')
        feels_temp = parameters[2]

    main_screen_textBox.insert(tk.END, " Humidity: " + str(parameters[3]) + "%" + '\n')

    condition = tk.Label(main_screen, text=parameters[5], font=('Helvetica',13),width=25)
    condition.place(x=415, y=210)

    sunrise_string=datetime.utcfromtimestamp(parameters[6]).strftime('%Y-%m-%d %H:%M:%S')
    sunrise_midle = str(int(sunrise_string[11:13]) + 3)
    sunrise_after = sunrise_string[13:18]
    sunrise_string=sunrise_midle + sunrise_after

    sunset_string = datetime.utcfromtimestamp(parameters[7]).strftime('%Y-%m-%d %H:%M:%S')
    sunset_middle = str(int(sunset_string[11:13]) + 3)
    sunset_after = sunset_string[13:18]
    sunset_string = sunset_middle + sunset_after

    main_screen_textBox.insert(tk.END, " Sunrise Time: " + sunrise_string + '\n')
    main_screen_textBox.insert(tk.END, " Sunset Time: " + sunset_string + '\n')
    main_screen_textBox.insert(tk.END, " Wind Speed: " + str(parameters[8]) + " m/s" + '\n')

    icon=ImageTk.PhotoImage(Image.open(requests.get(iconUrl.format(parameters[4]),stream=True).raw))
    icon_mainScreen.configure(image=icon)
    icon_mainScreen.image=icon

def CC_F_button_click():
    global is_celcious
    global temp
    if (is_celcious):
        temp = float((float(temp) * 9 / 5) + 32)
        temp = temp.__round__()
        is_celcious = False
        C_F_button.config(text='Fahrenheit')
        main_screen_textBox.delete('2.0','end')
        main_screen_textBox.insert('2.0', '\n')
        main_screen_textBox.insert('2.0', " Temperature: " + str(temp) + "°F" +'\n')
        if is_dropdown_used:
            temp_tempfelt = parameters[2]
            temp_felt_for_F = float((float(temp_tempfelt) * 9 / 5) + 32)
            main_screen_textBox.insert(tk.END, " Temperature felt: " + str(temp_felt_for_F) + "°F"  + '\n')
            main_screen_textBox.insert(tk.END, " Humidity: " + str(parameters[3]) + "%" + '\n')

            sunrise_string = datetime.utcfromtimestamp(parameters[6]).strftime('%Y-%m-%d %H:%M:%S')
            sunrise_midle = str(int(sunrise_string[11:13]) + 3)
            sunrise_after = sunrise_string[13:18]
            sunrise_string = sunrise_midle + sunrise_after

            sunset_string = datetime.utcfromtimestamp(parameters[7]).strftime('%Y-%m-%d %H:%M:%S')
            sunset_middle = str(int(sunset_string[11:13]) + 3)
            sunset_after = sunset_string[13:18]
            sunset_string = sunset_middle + sunset_after

            main_screen_textBox.insert(tk.END, " Sunrise Time: " + sunrise_string + '\n')
            main_screen_textBox.insert(tk.END, " Sunset Time: " + sunset_string + '\n')
            main_screen_textBox.insert(tk.END, " Wind Speed: " + str(parameters[8]) + " m/s" + '\n')

    else:

        temp = float(( float(temp) - 32) * 5 / 9)
        temp = temp.__round__()
        is_celcious = True
        C_F_button.config(text='Celsius')
        main_screen_textBox.delete('2.0', 'end')
        main_screen_textBox.insert('2.0', '\n')
        main_screen_textBox.insert('2.0', " Temperature: " + str(temp) + "°C" '\n')
        if is_dropdown_used:
            main_screen_textBox.insert(tk.END, " Temperature felt: " + str(parameters[2]) + "°C" + '\n')
            main_screen_textBox.insert(tk.END, " Humidity: " + str(parameters[3]) + "%" + '\n')

            sunrise_string = datetime.utcfromtimestamp(parameters[6]).strftime('%Y-%m-%d %H:%M:%S')
            sunrise_midle = str(int(sunrise_string[11:13]) + 3)
            sunrise_after = sunrise_string[13:18]
            sunrise_string = sunrise_midle + sunrise_after

            sunset_string = datetime.utcfromtimestamp(parameters[7]).strftime('%Y-%m-%d %H:%M:%S')
            sunset_middle = str(int(sunset_string[11:13]) + 3)
            sunset_after = sunset_string[13:18]
            sunset_string = sunset_middle + sunset_after

            main_screen_textBox.insert(tk.END, " Sunrise Time: " + sunrise_string + '\n')
            main_screen_textBox.insert(tk.END, " Sunset Time: " + sunset_string + '\n')
            main_screen_textBox.insert(tk.END, " Wind Speed: " + str(parameters[8]) + " m/s" + '\n')



main_screen = tk.Tk()
main_screen.title('Window')
main_screen.geometry('800x600')
main_screen.config(bg='black')

clicked=StringVar()
clicked.set('Cities')
dropdownlist_inMain_forId=tk.OptionMenu(main_screen,clicked,*dropdownlist_options_list,command=dropdown_clicked)
dropdownlist_inMain_forId.place(x=10, y=10)

C_F_button = tk.Button(main_screen, text="Celsius", width=20, command= CC_F_button_click ,font = ("Helvetica", 15))
C_F_button.place(x=415,y=10)

main_screen_textBox=tk.Text(main_screen,height=15,width=30)
main_screen_textBox.place(x=150,y=10)

icon_mainScreen=tk.Label(main_screen)
icon_mainScreen.place(x=475, y=75)
icon_mainScreen.config(bg='grey')

load_preferences()

main_screen.protocol("WM_DELETE_WINDOW",save_preferences_subMethod)


main_screen.mainloop()