import requests
import matplotlib.pyplot as plt
import pygame
import os
import math
import tkinter as tk
import datetime


def getWeather(lat, lon):
    api_key = "<YOUR API KEY>"
    exclude = "minutely,daily,alerts"

    url = 'https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude={}&appid={}'.format(lat, lon,
                                                                                                     exclude,
                                                                                                     api_key)
    res = requests.get(url)
    data = res.json()
    print(data)
    return data


def setup():

    latitude = 0
    longitude = 0
    # Initialize Pygame
    pygame.init()

    # Set window
    pygame.display.set_caption("Click on the map to get the latitude and longitude")

    # Load the world map image
    world_map = pygame.image.load("world_map.PNG")

    # Set the window size to match the size of the world map image
    SCREEN_WIDTH = world_map.get_width()
    SCREEN_HEIGHT = world_map.get_height()

    # Set the scaling factor
    LATITUDE_SCALE = 180 / SCREEN_HEIGHT
    LONGITUDE_SCALE = 360 / SCREEN_WIDTH


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 24)


    # Main loop
    while True:

        for event in pygame.event.get():
            # Check if the user clicked the close button
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Check if the user clicked the mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:

                print("Latitude: " + str(latitude))
                print("Longitude: " + str(longitude))

                return latitude, longitude
                #close map page
                pygame.quit()

        x, y = pygame.mouse.get_pos()
        # Convert the mouse coordinates to latitude and longitude
        latitude = (SCREEN_HEIGHT - y) * LATITUDE_SCALE - 90
        longitude = x * LONGITUDE_SCALE - 180

        Render = font.render("(" + (str(latitude)[:7]) + ", " + (str(longitude)[:7]) + ")", True, pygame.Color('black'))

        screen.blit(world_map, (0, 0))

        Rect = Render.get_rect()
        Rect.right = SCREEN_WIDTH - 20
        Rect.top = 20
        screen.blit(Render, Rect)

        pygame.display.update()

        clock.tick(60)


def graph():


    lat, lon = setup()

    with open("location.txt", "w") as file:
        # write the values to the file for update function below
        file.write("Latitude: {}\nLongitude: {}\n".format(lat, lon))


    weatherData = getWeather(lat, lon)

    temps = []
    times = []

    current_time = datetime.datetime.now()
    for i in range(6):
        temp = weatherData["hourly"][i]["temp"] - 273.15
        time = current_time + datetime.timedelta(hours=i)
        temps.append(temp)
        times.append(time)

    # Plot the temperature data
    plt.clf()
    plt.plot(times, temps)
    plt.xlabel("Time")
    plt.ylabel("Temperature (Celsius)")
    plt.title("Temperature over the Next 6 Hours")
    plt.savefig("graph.png")

    temp_kelvin = weatherData['current']['temp']
    currentTemp = "{:.1f}".format(temp_kelvin - 273.15) + '°C'
    weatherDescription = weatherData['current']['weather'][0]['main']
    location = weatherData['timezone']
    print(currentTemp)
    print(weatherDescription)

    return currentTemp, weatherDescription, location

#Run to update weather while not changing the region
def update():
    with open("location.txt", "r") as file:
        # read the contents of the location text file
        contents = file.read()

        # split the contents into lines
        lines = contents.split("\n")

        # get the latitude and longitude values
        lat = float(lines[0].split(": ")[1])
        lon = float(lines[1].split(": ")[1])

    weatherData = getWeather(lat, lon)

    # clear each list
    temps = []
    times = []

    # find temp for next 6 hours
    current_time = datetime.datetime.now()
    for i in range(6):
        temp = weatherData["hourly"][i]["temp"] - 273.15
        time = current_time + datetime.timedelta(hours=i)
        temps.append(temp)
        times.append(time)

    # Clear graph first
    plt.clf()
    # Plot the temperature data
    plt.plot(times, temps)
    plt.xlabel("Time")
    plt.ylabel("Temperature (Celsius)")
    plt.title("Temperature over the Next 6 Hours")
    plt.savefig("graph.png")

    # additional temp info
    temp_kelvin = weatherData['current']['temp']
    currentTemp = "{:.1f}".format(temp_kelvin - 273.15) + '°C'
    weatherDescription = weatherData['current']['weather'][0]['main']
    print(currentTemp)
    print(weatherDescription)

    # return additional info, no need to return graph since I have it as a file now
    return currentTemp, weatherDescription
