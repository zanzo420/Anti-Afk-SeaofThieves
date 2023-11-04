import sys
import keyboard
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from threading import Thread
import time
import random
import wmi
import win32gui

class AntiAfk(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.away = False
        self.target_window = None
        self.pid = None
        self.threadAfk = None
        self.keyListener = None
        self.listening = False

        self.toggle_button = QPushButton('AFK', self)
        self.toggle_button.clicked.connect(self.listenWindow)

        self.setWindowTitle('SoT Anti AFK')
        self.setGeometry(200, 200, 300, 100)
        self.show()

    def onKeyListener(self):
        while self.listening:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.scan_code > 0:
                    self.stopThread()
                    print("stopping")
                else:
                    pass                                        

    def is_sot_running(self) -> bool:
        try: 
            c = wmi.WMI()
            for process in c.Win32_Process(name="SoTGame.exe"):
                self.pid = process.ProcessId
                return True
            return False
        except Exception as error:
            print(error)
            return False

    def afk(self):
        while self.away and self.is_sot_running():
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

    def startThred(self):
        if not self.away:
            self.away = True
            self.listening = True
            self.threadAfk = Thread(target=self.afk)
            self.threadAfk.start()

    def stopThread(self):
        if self.away:
            self.away = False
            self.listening = False
            self.threadAfk.join()
            self.threadAfk = None
            self.toggle_button.setText('AFK')

    def listenWindow(self):
        if self.toggle_button.text() == 'AFK':
            #afk
            self.toggle_button.setText('Nicht AFK')
            print("afk")
            self.keyListener = Thread(target=self.onKeyListener)
            self.keyListener.start()
            self.startThred()
        else:
            #nicht afk
            self.toggle_button.setText('AFK')
            print("nicht afk")
            self.stopThread()
            self.keyListener.join()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AntiAfk()
    window.show()
    sys.exit(app.exec_())