import tkinter as tk
from tkinter import filedialog
import pygame
import os
from statistics import mode
import weather
import news
import time
import datetime
import random

global font

def main(currentTemp, weatherDescription, location):
    clock = pygame.time.Clock()

    # Initialize Pygame
    pygame.init()

    # Set the timer event ID
    TIMER_EVENT = pygame.USEREVENT + 1

    # Create a timer that will fire every 2 minutes
    pygame.time.set_timer(TIMER_EVENT, 2 * 60 * 1000)


    # Set up the screen
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("SJ - FridgeApp")

    bg = pygame.image.load("background.png")
    graphWidget = pygame.image.load("graph.png")
    newsWidget = pygame.image.load("headlines.png")
    n = random.randint(1,5)
    adWidget = pygame.image.load(f"ad{str(n)}.png")

    font = pygame.font.Font('freesansbold.ttf', 20)
    bigfont = pygame.font.Font('freesansbold.ttf', 25)

    # create text
    tempText = font.render('current temp: ' + currentTemp, True, (0,0,0))
    weatherText = font.render('current weather condition: ' + weatherDescription, True, (0, 0, 0))
    zoneText = font.render('location: ' + location , True, (0,0,0))
    updateText = bigfont.render('Update', True, (0,0,0))
    resetText = bigfont.render('Reset', True, (0,0,0))
    adtext = bigfont.render('New ad', True, (0,0,0))
    # create a rectangular object for button
    updateRect = pygame.Rect(30, 650, 200, 100)
    resetRect = pygame.Rect(250, 650, 200, 100)
    adRect = pygame.Rect(470, 650, 200, 100)



    #update ftn
    def update():

        currentTemp, weatherDescription = weather.update()
        tempText = font.render('current temp: ' + currentTemp, True, (0, 0, 0))
        weatherText = font.render('current weather condition: ' + weatherDescription, True, (0, 0, 0))
        graphWidget = pygame.image.load("graph.png")
        n = random.randint(1,5)
        adWidget = pygame.image.load(f"ad{str(n)}.png")

    # Main loop
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Button stuff
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] >= 30 and mouse_pos[0] <= 230 and mouse_pos[1] >= 650 and mouse_pos[1] <= 750:
                        update()

                    if mouse_pos[0] >= 250 and mouse_pos[0] <= 450 and mouse_pos[1] >= 650 and mouse_pos[1] <= 750:
                        pygame.quit()
                        setup()

                    if event.type == TIMER_EVENT:
                        update()

                    if mouse_pos[0] >= 470 and mouse_pos[0] <= 570 and mouse_pos[1] >= 650 and mouse_pos[1] <= 750:
                        n += 1
                        if n > 5:
                            n = 1

                        adWidget = pygame.image.load(f"ad{str(n)}.png")



        # Clear the screen
        screen.fill((255, 255, 255))
        screen.blit(bg, (0,0))

        now = datetime.datetime.now()

        # Render the time as text and in a good format
        time_text = font.render(now.strftime("%H:%M:%S"), True, (0, 0, 0))

        # Draw the time on the screen
        screen.blit(time_text, (30, 525))

        # Draw the image
        screen.blit(graphWidget, (30, 30))
        screen.blit(newsWidget, (650, 30))
        screen.blit(adWidget, (680, 520))

        # Draw button stuff
        pygame.draw.rect(screen, (200, 150, 100), updateRect)
        pygame.draw.rect(screen, (100, 200, 150), resetRect)
        pygame.draw.rect(screen, (100, 150, 200), adRect)
        screen.blit(zoneText, (30, 545))
        screen.blit(tempText, (30, 565))
        screen.blit(weatherText, (30, 585))
        screen.blit(updateText, (130 - (updateText.get_width() / 2), 700 - (updateText.get_height() / 2)))
        screen.blit(resetText, (350 - (resetText.get_width() / 2), 700 - (resetText.get_height() / 2)))
        screen.blit(adtext, (570 - (adtext.get_width() / 2), 700 - (adtext.get_height() / 2)))

        clock.tick(30)
        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()

#runs everything in order once
def setup():
    news.headlines()
    currentTemp, weatherDescription, location = weather.graph()
    main(currentTemp, weatherDescription, location)

#inital launch
setup()