import pyautogui
import sys
from pywinauto import Application
import keyboard
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import pygetwindow as gw
import psutil
from threading import Thread
import time
import random
import win32com.client
import string

class AntiAfk(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.away = False
        self.target_window = None
        self.pid = None
        self.threadAfk = None

        self.toggle_button = QPushButton('AFK', self)
        self.toggle_button.clicked.connect(self.listenWindow)

        self.setWindowTitle('SoT Anti AFK')
        self.setGeometry(100, 100, 300, 100)
        self.show()

        keyListener = Thread(target=self.onKeyListener)
        keyListener.start()


    def onKeyListener(self):
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                badKeys = ['w', 'a', 's', 'd']
                for i in badKeys:
                    if event.name in string.punctuation or event.name in string.whitespace:
                        self.away = False
                        break
                    elif i in event.name:
                        self.away = True
                        break
                    else:
                        self.away = False
                print(self.away)

    # in linie 43 ob der gedrückte knopf ein spezieller char ist wie strg oder so geht wahrescheinlich so das du nur event hinschreibst aber mach ich heute nicht mehr lol
                                        


    def is_sot_running(self) -> bool:
        try: 
            wmi = win32com.client.GetObject("winmgmts:")
            for process in wmi.InstancesOf("Win32_Process"):
                if process.Properties_("Name").Value.lower() == "discord.exe".lower():
                    self.pid = process.Properties_['ProcessId'].Value
                    return True
                else:
                    pass
            return False
        except Exception as error:
            print(error)
            return False

    def afk(self):
        while self.away and self.is_sot_running():
            try:
                print(self.pid)
                app = Application().connect(process=self.pid)
                app.top_window().set_focus()

                keys = ['w', 'a', 's', 'd']
                random.shuffle(keys)
                for key in keys:
                    pyautogui.press(key)
                    time.sleep(random.uniform(0.05, 2))

            except Exception as error:
                print(error)
                pass

    def startThred(self):
        if not self.away:
            self.away = True
            self.threadAfk = Thread(target=self.afk)
            self.threadAfk.start()

    def stopThread(self):
        if self.away:
            self.away = False
            self.threadAfk.join()
            self.threadAfk = None

    def listenWindow(self):
        if self.toggle_button.text() == 'AFK':
            #afk
            self.toggle_button.setText('Nicht AFK')
            print("afk")
            self.startThred()
        else:
            #nicht afk
            self.toggle_button.setText('AFK')
            print("nicht afk")
            self.stopThread()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AntiAfk()
    window.show()
    sys.exit(app.exec_())