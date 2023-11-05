import math, time, keyboard
import pyautogui as pagui
from PIL import Image, ImageGrab

def get_pixel(img, pt_x, pt_y):             # Method to return pixel value given an image and the X and Y coordinates
    pixel_matrix = img.load()               # Loads the image as a matrix of pixels
    return pixel_matrix[pt_x, pt_y]         # Returns the exact pixel value at the given points



def play():
    pt_x, pt_y, width, height = 0, 102, 1900, 872       # Store the exact position of the dino game within a 1920-pixel-width window

    jump_time = 0                                       # Store time intervals
    last_jump_time = 0
    cur_jump_time = 0
    last_interval_time = 0
    y_sc1, y_sc2, x_start, x_end = 557, 486, 400, 415   # Positions where obstacles may appear (relative to window size and placement)
    y_sc_bird = 460                                     # Usual Y position for birds to spawn

    time.sleep(5)                                       # When starting the bot, give the user time to switch to Chrome and start the game

    while True:
        t1 = time.time()

        if keyboard.is_pressed("e"):                # Press space to stop the bot
            break
        
        screenshot = pagui.screenshot(region=(pt_x, pt_y, width, height))       # Screenshot the game window to process
        screenshot.save("dinogame.jpg")
        bgcol = get_pixel(screenshot, 100, 100)         # Get the background color of the screenshot

        for i in range (x_end, x_start, -1):
            if (get_pixel(screenshot, i, y_sc1) != bgcol) or (get_pixel(screenshot, i, y_sc2) != bgcol):
                keyboard.press('up')                    # Jump if a cactus is detected
                jump_time = time.time()                 # Store the jump timeframe
                cur_jump_time = jump_time
                break
            if (get_pixel(screenshot, i, y_sc_bird) != bgcol):
                keyboard.press('down')                  # Duck if a bird is detected
                time.sleep(0.4)                         # Wait for the bird to pass
                keyboard.release('down')                # Let go of duck key
                break

            interval_time = cur_jump_time - last_jump_time
            if last_interval_time != 0 and math.floor(interval_time) != math.floor(last_interval_time):     # This checks if the time between current and last jump frames are the same. If they're not, the game is speeding up.
                x_end += 4                              # Increase the scanning range on the x_axis to accommodate for the increasing game speed
                if x_end >= width:                      # Limit the value of the x axis range to window width
                    x_end = width

            last_jump_time = jump_time                  # Update jump time & interval timeframe values
            last_interval_time = interval_time

play()