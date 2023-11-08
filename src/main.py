import sys
import keyboard
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from threading import Thread
import time
import random
import wmi
import win32gui
import pythoncom

class AntiAfk(QMainWindow):
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
        self.images = [QPixmap('images/notafk.png'), QPixmap('images/afk.png')]
        self.current = 0
        self.current_image = self.images[self.current]
        self.afktext = ["Not AFK", "AFK"]
        self.current_text = self.afktext[0]

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.setWindowTitle('SoT Anti AFK')
        self.setGeometry(500, 500, 400, 400)
        self.setMinimumSize(400, 300)
        color = '#000000'
        self.setStyleSheet(f'background-color: {color};')
        self.label = QLabel(self)
        self.label.setGeometry(0, 0 , 400, 400)
        self.label.setPixmap(self.images[0])
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignCenter)
        
        self.textfield = QLabel("Not AFK")
        self.textfield.setStyleSheet("color: red")
        #self.textfield.setStyleSheet("font-size: 20px;")
        self.textfield.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)
        layout.addWidget(self.textfield)
        central_widget.setLayout(layout)

        self.label.mousePressEvent = self.listenWindow

        self.show()
        
    def resizeEvent(self, event):
        new_width = self.width()
        new_height = self.height()
        
        if new_width * self.images[0].height() > new_height * self.images[0].width():
            new_width = (new_height * self.images[0].width()) // self.images[0].height()
        else:
            new_height = (new_width * self.images[0].height()) // self.images[0].width()

        self.label.setGeometry(0, 0, new_width, new_height)
        self.label.setPixmap(self.images[0].scaled(new_width, new_height))

    def onKeyListener(self):
        while self.listening:
            print("running")
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
        while self.away:
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

    def changeText(self):
        if self.current == 0:
            self.textfield.setText("Not AFK")
        else:
            self.textfield.setText("AFK")

    def startThred(self):
        if self.is_sot_running():
            self.changeText()
            self.away = True
            self.listening = True
            self.threadstopper = True
            self.threadAfk = Thread(target=self.afk)
            self.threadAfk.start()
            print("AFK")
        else:    
            print("Your Sea of Thieves is not Running")
            self.stopThread()
        

    def stopThread(self):
        try:
            print("Not AFK")
            self.away = False
            self.listening = False
            self.label.setPixmap(self.images[0])
            self.current = 0
            self.threadstopper = False
            self.changeText()
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
            self.stopThread()
        else:
            #afk
            self.keyListener = Thread(target=self.onKeyListener)
            self.startThred()
            self.keyListener.start()    
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AntiAfk()
    window.show()
    sys.exit(app.exec_())