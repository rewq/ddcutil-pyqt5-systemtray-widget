from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import Qt
import subprocess
import os 

def getbrightness(cmd="ddcutil -b 16 --brief getvcp 10 | cut -d ' ' -f4"):
    process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)

    # wait for the process to terminate
    out, err = process.communicate()
    errcode = process.returncode

    return int(out.decode().strip())

def setbrightness(brightness_value,cmd="ddcutil -b 16 --brief setvcp 10 "):
    process = subprocess.Popen(cmd+str(brightness_value), shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)

    # wait for the process to terminate
    out, err = process.communicate()
    errcode = process.returncode

    return errcode

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
        setbrightness(slider.value())

def actionTrayActivacted(reason):
	if reason == QSystemTrayIcon.MiddleClick:
		QApplication.quit()
	elif reason == QSystemTrayIcon.Trigger:
		cur_brightness = getbrightness()
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