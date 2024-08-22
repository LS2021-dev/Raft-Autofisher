import threading
from time import sleep

import pyautogui as auto
from PIL import ImageGrab
from pynput import keyboard
from pynput.keyboard import KeyCode


def check_fishing():  # Captures Image, Returns True If Fishing Box Found
    capture = ImageGrab.grab(bbox=(938, 450, 980, 475))  # Left, Upper, Right, Lower

    # Grabs the RGB Codes For the 2 Most Prevalent Colors Within The Screen Clip
    # As the Correct Screen Clip Should Only Contain 2 Colors, This Seems to Work Decently Well
    colors = capture.quantize(colors=2, method=2).getpalette()[:6]

    # Compare Them To The Fishing Box Colors
    return colors == [229, 211, 180, 85, 37, 8]


def fish():  # Run The Auto Fisher - This Will Be Run as A Thread
    while True:
        global running
        while running:
            # Full Cast before starting the loop
            auto.mouseDown()
            sleep(1.7)
            auto.mouseUp()
            sleep(0.5)

            while running:
                if check_fishing():
                    # Catch Fish
                    auto.click()
                    sleep(0.5)

                    # Full Cast
                    auto.mouseDown()
                    sleep(1.7)
                    auto.mouseUp()
                    sleep(0.5)
                sleep(0.5)
        sleep(1)


trigger_key = KeyCode.from_char('l')


print(f"Auto Fisher Starting, press {trigger_key} to toggle")
print("Fishing:", False)
running = False
fisher = threading.Thread(target=fish)
fisher.start()


# Callback Function To Toggle Fisher
def toggle(key):
    if key == trigger_key:
        global running
        print("Fishing:", not running)
        running = not running

# Blocking Keyboard Listener
with keyboard.Listener(on_press=toggle) as listener:
    listener.join()
