import sys
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
 
# create our window
app = QApplication(sys.argv)
w = QWidget()
w.resize(300, 300)
w.setWindowTitle('Laborantul Destept')
w.setStyleSheet("background-color:black;")
 
# Create a button in the window
btn = QPushButton('Press me!', w)
btn.setToolTip('Hold pressed for recording')
#btn.clicked.connect(exit)
btn.resize(btn.sizeHint())
btn.move(100, 100)
btn.setStyleSheet(''' background-color: red;
 border-style: solid;
 border-width:1px;
 border-radius:50px;
 border-color: red;
 max-width:100px;
 max-height:100px;
 min-width:100px;
 min-height:100px;''')
 
# Create the actions
@pyqtSlot()
def on_click():
    print('clicked')
 
@pyqtSlot()
def on_press():
    print('pressed')
 
@pyqtSlot()
def on_release():
    print('released')
 
# connect the signals to the slots
btn.clicked.connect(on_click)
btn.pressed.connect(on_press)
btn.released.connect(on_release)
 
# Show the window and run the app
w.show()
app.exec_()