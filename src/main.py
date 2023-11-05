import sys
import keyboard
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from threading import Thread
import time
import random
import wmi
import win32gui
import pythoncom

class AntiAfk(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.away = False
        self.target_window = None
        self.pid = None
        self.threadAfk = None
        self.keyListener = None
        self.listening = False
        self.threadstopper = True
        self.switch = True
        self.images = [QPixmap('images/gus.PNG'), QPixmap('images/idk.png')]
        self.current = 0
        self.current_image = self.images[self.current]

        self.setWindowTitle('SoT Anti AFK')
        self.label = QLabel(self)
        self.label.setGeometry(200,200,200,100)
        self.label.setPixmap(self.images[0])
        self.label.setAlignment(Qt.AlignCenter)
        self.label.mousePressEvent = self.listenWindow

        self.setFixedSize(400, 300)
        self.show()

    def onKeyListener(self):
        while self.listening and self.threadstopper:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.scan_code > 0:
                    self.stopThread()
                    print("stopping")
                else:
                    pass                                        

    def is_sot_running(self) -> bool:
        pythoncom.CoInitialize()
        try: 
            c = wmi.WMI()
            for process in c.Win32_Process(name="SoTGame.exe"):
                self.pid = process.ProcessId
                pythoncom.CoUninitialize()
                return True
            pythoncom.CoUninitialize()
            return False
        except Exception as error:
            print(error)
            return False

    def afk(self):
        while self.away and self.is_sot_running() and self.threadstopper:
            try: 
                keys = ['w', 'a', 's', 'd']
                random.shuffle(keys)
                for key in keys:
                    sotWindow = win32gui.FindWindow("ApplicationFrameWindow", "Sea of Thieves")
                    win32gui.SetForegroundWindow(sotWindow)
                    keyboard.press(key)
                    time.sleep(random.uniform(0.05, 2))
                    keyboard.release(key)

            except Exception as error:
                print(error)
                pass
        if self.is_sot_running() == False:
            print("Your Sea of Thieves is not Running")
            self.stopThread()


    def startThred(self):
        if not self.away:
            self.away = True
            self.listening = True
            self.threadstopper = True
            self.threadAfk = Thread(target=self.afk)
            self.threadAfk.start()

    def stopThread(self):
        if self.away:
            try:
                self.away = False
                self.listening = False
                self.label.setPixmap(self.images[0])
                self.current = 0
                self.threadstopper = False
                self.keyListener.join()
                self.threadAfk.join()
                self.threadAfk = None
                self.keyListener = None
            except:
                pass

    def listenWindow(self, event):
        self.current = (self.current + 1) % len(self.images)
        self.current_image = self.images[self.current]
        self.label.setPixmap(self.current_image)

        if self.current == 0:
            # nicht afk
            print("Not AFK")
            self.stopThread()
        else:
            #afk
            print("AFK")
            self.keyListener = Thread(target=self.onKeyListener)
            self.startThred()
            self.keyListener.start()    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AntiAfk()
    window.show()
    sys.exit(app.exec_())