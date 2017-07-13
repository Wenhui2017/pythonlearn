import sys
from PyQt5 import QtCore, QtGui, QtPrintSupport, QtWidgets, uic

from_class = uic.loadUiType("tempconv_menu_hotkeys.ui")[0]

class MyWindowClass(QtWidgets.QMainWindow, from_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btn_CtoF.clicked.connect(self.btn_CtoF_clicked)
        self.btn_FtoC.clicked.connect(self.btn_FtoC_clicked)
        self.action_CtoF.triggered.connect(self.btn_CtoF_clicked)
        self.action_FtoC.triggered.connect(self.btn_FtoC_clicked)
        self.actionExit.triggered.connect(self.menuExit_selected)

    def btn_CtoF_clicked(self):
        cel = float(self.editCel.text())
        fahr = cel * 9.0 / 5 + 32
        self.spinFahr.setValue(int(fahr + 0.5))
        print ('cel = ', cel, 'fahr = ', fahr)

    def btn_FtoC_clicked(self):
        fahr = self.spinFahr.value()
        cel = (fahr - 32) * 5 / 9.0
        cel_text = '%.2f' % cel
        self.spinFahr.setText(cel_text)

    def menuExit_selected(self):
        self.close()
         
        
app = QtWidgets.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
