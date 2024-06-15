import pyautogui
import time
from PIL import Image
import pygetwindow as gw
from pynput import mouse


class Calibration:
    def __init__(self):
        self.coordinates = []
        self.listener = mouse.Listener(on_click=self.on_click)

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.right and not pressed:
            print(f'Mouse clicked at ({x}, {y}) with right button')
            self.coordinates.append((x, y))
            if len(self.coordinates) == 2:
                self.calculate_distance()
                return False  # Stop listener

    def calculate_distance(self):
        if len(self.coordinates) == 2:
            x1, y1 = self.coordinates[0]
            x2, y2 = self.coordinates[1]
            distances = abs(x2 - x1)
            return distances
            # print(f'Distance between the two points in the x-coordinate: {distance}')

    def start(self):
        self.listener.start()
        self.listener.join()
        return self.calculate_distance()


def take_window_screenshot(window_title):
    # Get the window by title
    window = gw.getWindowsWithTitle(window_title)[0]
    region = (155, 203, 1570, 800)
    # Activate the window (bring it to the front)
    window.activate()
    # time.sleep(5)

    left = window.left + region[0]
    top = window.top + region[1]
    width = region[2]
    height = region[3]
    # Take a screenshot of the window
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    return screenshot


def move_until_color(move_step):
    time.sleep(3)  # Wait for 5 seconds before starting

    # Get the current mouse position
    current_x, current_y = pyautogui.position()
    step_distance = move_step
    y_step = move_step
    x_coord = 0
    y_coord = 0
    i = 0
    k = 0

    while True:
        start_screenshot = take_window_screenshot("AntilatencyService")
        screenshot_name = f"data/{x_coord}_{y_coord}.png"
        start_screenshot.save(screenshot_name)

        pyautogui.mouseDown(button='middle')
        pyautogui.moveTo(current_x + step_distance, current_y)
        time.sleep(0.01)  # Small delay to allow the mouse to move
        pyautogui.mouseUp(button='middle')
        pyautogui.moveTo(current_x, current_y)
        i = i + 1
        x_coord += step_distance

        if i >= width_zone / step_in_cells:

            pyautogui.mouseDown(button='middle')
            pyautogui.moveTo(current_x, current_y + y_step)
            time.sleep(0.01)
            pyautogui.mouseUp(button='middle')
            time.sleep(0.01)
            pyautogui.moveTo(current_x, current_y)
            y_coord += y_step
            step_distance = -step_distance
            i = 0
            k = k + 1
            if k >= height_zone / step_in_cells:
                return


width_zone = 25
height_zone = 32
step_in_cells = 5

calibration = Calibration()
distance = -calibration.start()

move_until_color(distance)
