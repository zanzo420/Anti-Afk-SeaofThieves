import pyautogui
from pynput import keyboard
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import pygetwindow as gw
import psutil
from threading import Thread
import time
import random
import win32com.client

class AntiAfk():
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

        self.away = False
        self.listening = True
        self.target_window = None
        self.pid = None
        #keyboard.hook(self.onKeyListener())
        
        #threadKeyListener = Thread(target=self.onKeyListener())
        thread = Thread(target=self.interface())
        thread.start()
        threadKeyListener.start()
        
    def interface(self):
        root = tk.Tk()
        root.geometry(f"{self.width}x{self.height}")
        root.title("Anti-Afk SoT")
        image = PhotoImage(file="images\gus.PNG")
        label = tk.Label(root, image=image)
        button1 = tk.Button(root, text="Start", command=lambda: self.listen("start"))
        button2 = tk.Button(root, text="Stop", command=lambda: self.listen("stop"))
        label.pack()
        button1.pack(side=tk.LEFT)
        button2.pack(side=tk.RIGHT)
        root.mainloop()

    def onKeyListener(self, e) -> bool:
        if e.event_type == keyboard.KEY_DOWN:
            print("key")
            self.away = False

    def is_sot_running(self) -> bool:
        try: 
            wmi = win32com.client.GetObject("winmgmts:")
            for process in wmi.InstancesOf("Win32_Process"):
                if process.Properties_("Name").Value.lower() == "discord.exe".lower():
                    self.pid = process.Properties_['ProcessId'].Value
                    print(self.pid)
                    return True
                else:
                    pass
            return False
        except Exception as error:
            print(error)
            return False

    def afk(self):
        if self.away and self.is_sot_running():
            try:
                for window in gw.getAllTitles():
                    if gw.getWindowsWithTitle(window)[0].pid == 17816:
                        window_pid = gw.getWindowsWithTitle(window)
                        if window_pid:
                            window.maximize()

                            keys = ['w', 'a', 's', 'd']
                            for key in keys:
                                print(key)
                                pyautogui.press(key)
                                time.sleep(random.uniform(0.05, 2))

            except Exception as error:
                print(error)

    def listen(self, status):
        if "start" in status and self.listening == True:
            self.listening = False
            print("Start")
            self.away = True
            while self.away:
                threadAfk = Thread(target=self.afk())
                threadAfk.start()
            print(self.pid)
        elif "stop" in status:
            print("Stop")
            self.listening = True
            self.away = False


    def test(self):
        if self.is_sot_running():
            print("running")
        else:
            print("not running")


if __name__ == "__main__":
    app = AntiAfk(300, 500)