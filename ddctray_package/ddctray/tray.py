from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
import subprocess
import os 
import sys
from ddctray.libddcutil import *

busno = getBusnoFromModel("DELL U3219Q")

if not busno:
    exit(1)

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

window = QWidget()
window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Popup)
layout = QVBoxLayout()
slider = QSlider()
slider.setTracking(True)
slider.setRange(0, 100)
label = QLabel("??")
label.setStyleSheet(''' font-size: 16px; ''')
label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
label.setMinimumWidth(50)
layout.addWidget(slider,alignment=Qt.AlignHCenter)
layout.addWidget(label)
window.setLayout(layout)

def centerWindow(w=window):
    cpos = QCursor().pos()
    w.move(cpos.x()-int(w.width()/2),cpos.y()-w.height()-8)

def updateLabel(value):
        label.setText(str(value)+"%")

def updateBrightness():
        setbrightness(busno,slider.value())

def actionTrayActivacted(reason):
    if reason == QSystemTrayIcon.MiddleClick:
        QApplication.quit()
    elif reason == QSystemTrayIcon.Trigger:
        window.setVisible(not window.isVisible())
        centerWindow()
        cur_brightness = getbrightness(busno)
        label.setText(str(cur_brightness)+"%")
        slider.setValue(cur_brightness)

def actionTrayActivactede(e):
    print(e)
# Adding an icon
icon = QIcon(os.path.join(os.path.dirname(__file__),'inc','light-bulb.png'))

# Adding item on the menu bar
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)
  
# Creating the options
menu = QMenu()
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)
  
# Adding options to the System Tray
tray.setContextMenu(menu)
tray.activated.connect(actionTrayActivacted)
slider.valueChanged.connect(updateLabel)
slider.sliderReleased.connect(updateBrightness)
 
def run():      
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
