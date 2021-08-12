from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import Qt
import subprocess
import os 
from libddcutil import *

busno = getBusnoFromModel("DELL U3219Q")

if not busno:
	exit(1)

app = QApplication(["testname"])
app.setQuitOnLastWindowClosed(False)

window = QWidget()
window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Popup)
layout = QVBoxLayout()
slider = QSlider()
slider.setTracking(True)
label = QLabel("??")
label.setStyleSheet(''' font-size: 16px; ''')
layout.addWidget(slider)
layout.addWidget(label)
window.setLayout(layout)

def centerWindow(w=window):
	frameGm = window.frameGeometry()
	screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
	centerPoint = QApplication.desktop().screenGeometry(screen).center()
	frameGm.moveCenter(centerPoint)
	window.move(frameGm.topLeft())

def updateLabel(value):
        label.setText(str(value))

def updateBrightness():
        setbrightness(busno,slider.value())

def actionTrayActivacted(reason):
	if reason == QSystemTrayIcon.MiddleClick:
		QApplication.quit()
	elif reason == QSystemTrayIcon.Trigger:
		cur_brightness = getbrightness(busno)
		label.setText(str(cur_brightness))
		slider.setValue(cur_brightness)
		window.setVisible(not window.isVisible())
		centerWindow()

# Adding an icon
icon = QIcon(os.path.join( os.getcwd(), 'light-bulb.svg' ))
  
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

app.exec_()