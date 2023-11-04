import win32gui
import win32con
import pyautogui
import time

pid = 17844 

try:
    x=win32gui.FindWindow("ApplicationFrameWindow", "Sea of Thieves")
    print(x)
    win32gui.SetForegroundWindow(x)
    pyautogui.sleep(1)
    pyautogui.press('space')
except Exception as e:
    print(f"Fehler beim Fokussieren der Anwendung: {str(e)}")