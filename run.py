import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from classMaker import SQLClassMaker
class window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400,200)
        self.gui()
        self.classMaker = None
    def gui(self):
        self.mainFrame = QFrame(self)
        self.mainFrame.resize(self.size())

        self.hostedit = QLineEdit()
        self.hostedit.setPlaceholderText("Default is localhost")
        self.hostlabel = QLabel("Host:")

        self.usredit = QLineEdit()
        self.usredit.setPlaceholderText("Default is root")
        self.usrlabel = QLabel("User:")

        self.psswdedit = QLineEdit()
        self.psswdedit.setPlaceholderText("Default is empty")
        self.psswdedit.setEchoMode(QLineEdit.Password)
        self.psswdlabel = QLabel("Password:")

        self.packageedit = QLineEdit()
        self.packageedit.textChanged.connect(self.onTextChanged)
        self.packagelabel = QLabel("Package:")

        self.dbLabel = QLabel('Select DB:')
        self.dbComboBox = QComboBox()

        self.nextButton = QPushButton("Next")
        self.nextButton.setDisabled(True)
        self.nextButton.clicked.connect(self.onClickNext)


        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.onClickStart)

        self.mainLayout = QGridLayout(self)

        
        self.mainLayout.addWidget(self.hostlabel,0,0)
        self.mainLayout.addWidget(self.hostedit,0,1)

        self.mainLayout.addWidget(self.usrlabel,1,0)
        self.mainLayout.addWidget(self.usredit,1,1)

        self.mainLayout.addWidget(self.psswdlabel,2,0)
        self.mainLayout.addWidget(self.psswdedit,2,1)

        self.mainLayout.addWidget(self.packagelabel,3,0)
        self.mainLayout.addWidget(self.packageedit,3,1)

        self.mainLayout.addWidget(self.nextButton,4,0,1,0)

        self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.setContentsMargins(20,20,20,20)
        self.mainLayout.setHorizontalSpacing(50)
        self.mainLayout.setVerticalSpacing(15)

        self.mainFrame.setLayout(self.mainLayout)
    def resizeEvent(self, event):
        self.mainFrame.resize(self.size())
    def onClickNext(self):
        self.packageName = self.packageedit.text()
        self.classMaker = SQLClassMaker(self.hostedit.text(),self.usredit.text(),self.psswdedit.text())
        self.mainLayout.removeWidget(self.hostlabel)
        self.hostlabel.deleteLater()
        self.mainLayout.removeWidget(self.hostedit)
        self.hostedit.deleteLater()
        self.mainLayout.removeWidget(self.usrlabel)
        self.usrlabel.deleteLater()
        self.mainLayout.removeWidget(self.usredit)
        self.usredit.deleteLater()
        self.mainLayout.removeWidget(self.psswdedit)
        self.psswdedit.deleteLater()
        self.mainLayout.removeWidget(self.psswdlabel)
        self.psswdlabel.deleteLater()
        self.mainLayout.removeWidget(self.packageedit)
        self.packageedit.deleteLater()
        self.mainLayout.removeWidget(self.packagelabel)
        self.packagelabel.deleteLater()
        self.mainLayout.removeWidget(self.nextButton)
        self.nextButton.deleteLater()
        self.mainLayout.removeWidget(self.usrlabel)
        self.mainLayout.addWidget(self.dbLabel,0,0)
        dbs = self.classMaker.getDbs();
        if dbs == None:
            sys.exit(0)
        for db in dbs:
            self.dbComboBox.addItem(db)
        self.mainLayout.addWidget(self.dbComboBox,0,1)
        self.mainLayout.addWidget(self.startButton,1,0,1,0)
    def onClickStart(self):
        self.classMaker.exportClass(self.classMaker.getTables(self.dbComboBox.currentText()),self.packageName)
        self.classMaker.closeCon()
        self.classMaker.exit()
    def onTextChanged(self,event):
        if self.packageedit.text() == '':
            self.nextButton.setDisabled(True)
        else:
            self.nextButton.setDisabled(False)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = window()
    gui.show()
    app.exec_()