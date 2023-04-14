from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QTextEdit, QLabel, QFileDialog, QHBoxLayout, QVBoxLayout,
    QTreeWidget, QMenuBar, QStatusBar, QPushButton, QCheckBox, 
    QComboBox, QFontComboBox,
    QTreeWidgetItem, QMenu, QAction, QDialog)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys
import time
import platform

STATUSBAR = f" {time.ctime()} | {platform.system()} "

MOUNTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

CD = [(time.asctime()).split()[4], (time.asctime()).split()[1], (time.asctime()).split()[2]]

tasks = {}

with open("style/white.css", 'r') as f:
    whiteTheme = f.read()
with open("style/black.css", 'r') as f:
    blackTheme = f.read()

with open("style/whiteWindow.css", 'r') as f:
    whiteThemeWindow = f.read()
with open("style/blackWindow.css", 'r') as f:
    blackThemeWindow = f.read()



class Task():
    def __init__(self, date, index, context, state=True):
        self.date = date
        self.index = index
        self.context = context
        self.state = state
    def setContext(self, context):
        self.context = context
    def setState(self, state):
        self.state = state
    

class UI(QMainWindow):
    currentIndex = -1
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("app.ui", self)
        self.setWindowTitle(f"{CD[2]} {CD[1]} {CD[0]}")
        self.setStyleSheet(whiteTheme)
        """ Main elements"""
        self.menubar = self.findChild(QMenuBar, "menubar")
        self.statusbar = self.findChild(QStatusBar, "statusbar")
        self.taskBlock = self.findChild(QTextEdit, "taskBlock")
        self.treeBlock = self.findChild(QTreeWidget, "treeBlock")
        self.btnCreateTask = self.findChild(QPushButton, "createTask")
        """Action element in menubar"""
        """File section"""
        self.saveTask = self.findChild(QAction, "actionSaveTask")
        self.openToFileTask = self.findChild(QAction, "actionOpentaskfromtxtfile")
        self.saveToFileTask = self.findChild(QAction, "actionSavetaskintxtfile")
        self.exit = self.findChild(QAction, "actionExit")
        """Edit"""
        self.aUndo = self.findChild(QAction, "actionUndo")
        self.aRedo = self.findChild(QAction, "actionRedo")
        self.aCut = self.findChild(QAction, "actionCut")
        self.aCopy = self.findChild(QAction, "actionCopy")
        self.aPaste = self.findChild(QAction, "actionPaste")
        """Appearance"""
        self.changeTheme = self.findChild(QAction, "actionChangeTheme")
        self.changeFont = self.findChild(QAction, "actionChangeFont")
        """About"""
        self.about = self.findChild(QMenu, "menuAbout")
        

        self.labelsb = QLabel(STATUSBAR)
        self.statusbar.addWidget(self.labelsb)
        self.treeBlock.setHeaderLabel(CD[0])
        self.treeBlock.itemClicked.connect(self.changeCurrentTask)
        self.btnCreateTask.clicked.connect(self.toCreateTask)
        self.currentIndex += 1
        self.upTree()

        self.saveTask.triggered.connect(self.saveTask_)
        self.openToFileTask.triggered.connect(self.openToFileTask_)
        self.saveToFileTask.triggered.connect(self.saveToFileTask_)
        self.aUndo.triggered.connect(self.aUndo_)
        self.aRedo.triggered.connect(self.aRedo_)
        self.aCut.triggered.connect(self.aCut_)
        self.aCopy.triggered.connect(self.aCopy_)
        self.aPaste.triggered.connect(self.aCopy_)
        self.changeTheme.triggered.connect(self.changeTheme_)
        self.changeFont.triggered.connect(self.changeFont_)
        self.exit.triggered.connect(self.exit_)
        self.about.triggered.connect(self.about_)
    
        self.treeBlock.itemChanged.connect(self.checked)

    def upTree(self):
        for mountly in MOUNTHS:
            item = QTreeWidgetItem([mountly])
            self.treeBlock.addTopLevelItem(item) 
    def toCreateTask(self):
        if tasks and CD[2] != tasks.keys():
                tasks[CD[2]].setContext(self.taskBlock.toPlainText())
        else:
            tasks[CD[2]] = Task(CD, self.currentIndex, self.taskBlock.toPlainText(), False)
            self.addTaskToTree(self.treeBlock.invisibleRootItem(), tasks[CD[2]])
        print(tasks)
        print(CD)

    def addTaskToTree(self, tree, item):
        for i in range(tree.childCount()):
            child = tree.child(i).text(0)
            if item.date[1] == child:
                treeitem = QTreeWidgetItem([str(item.date[2])])
                treeitem.setCheckState(0, Qt.Unchecked)
                treeitem.setBackground(0, QColor(0, 0, 0, 127))
                tree.child(i).addChild(treeitem)
    def changeCurrentTask(self):
        if self.treeBlock.currentItem() != None:
            if self.treeBlock.currentItem().text(0) in MOUNTHS:
                pass
            else:
                self.setWindowTitle(f" {tasks[self.treeBlock.currentItem().text(0)].date[2]} {tasks[self.treeBlock.currentItem().text(0)].date[1]} {tasks[self.treeBlock.currentItem().text(0)].date[0]}")
                self.taskBlock.setPlainText(tasks[self.treeBlock.currentItem().text(0)].context)

    def saveTask_(self): pass
    def openToFileTask_(self):
        fname = QFileDialog.getOpenFileName(self, "File name")
        if fname[0] != '':
            with open(str(fname[0]), 'r') as f:
                self.taskBlock.setPlainText(f.read())
            
    def saveToFileTask_(self):
        fname = QFileDialog.getSaveFileName(self, "File name")
        if fname[0] != '':
            with open(str(fname[0]), 'w') as f:
                f.write(self.taskBlock.toPlainText())
                f.close()
    def aUndo_(self):
        self.taskBlock.undo()
    def aRedo_(self):
        self.taskBlock.redo()
    def aCut_(self):
        self.taskBlock.cut()
    def aCopy_(self):
        self.taskBlock.copy()
    def aPaste_(self):
        self.taskBlock.paste()
    def changeTheme_(self):
            self.changeThemeWindow = QDialog()
            self.changeThemeWindow.setStyleSheet(whiteThemeWindow)
            layout = QHBoxLayout(self.changeThemeWindow)
            black = QPushButton("black")
            black.clicked.connect(self.toBlack)
            white = QPushButton("white")
            white.clicked.connect(self.toWhite)
            close = QPushButton("Close")
            close.clicked.connect(lambda: self.changeThemeWindow.accept())

            layout.addWidget(black)
            layout.addWidget(white)
            layout.addWidget(close)
            self.changeThemeWindow.setWindowTitle("Change Theme")
            self.changeThemeWindow.exec()

    def toBlack(self):
         self.setStyleSheet(blackTheme)
         self.changeThemeWindow.setStyleSheet(blackThemeWindow)
    def toWhite(self):
         self.setStyleSheet(whiteTheme)
         self.changeThemeWindow.setStyleSheet(whiteThemeWindow)

    def changeFont_(self):
            self.changeFontWindow = QDialog()
            self.changeFontWindow.setStyleSheet(whiteThemeWindow)
            self.fonts = QFontComboBox()
            self.fontsize = QComboBox()
            self.fontsize.addItems([str(i*5) for i in range(1, 10)])
            self.layoutv = QVBoxLayout()
            self.layouth = QHBoxLayout()
            ok = QPushButton("Ok")
            close = QPushButton("Close")
            ok.clicked.connect(self.newFont)
            close.clicked.connect(lambda: self.changeFontWindow.accept())
            
            self.layouth.addWidget(self.fonts)
            self.layouth.addWidget(self.fontsize)
            self.layoutv.addLayout(self.layouth)
            self.layoutv.addWidget(close)
            self.layoutv.addWidget(ok)
            self.changeFontWindow.setLayout(self.layoutv)
            self.changeFontWindow.setWindowTitle("Change Font")
            self.changeFontWindow.exec()
    def newFont(self):
        self.font = self.fonts.currentText()
        self.fsize = int(self.fontsize.currentText())
        print(f"{self.font} -- {self.fsize}")
        newfont = QFont(self.font, self.fsize)
        self.taskBlock.setFont(newfont)
        self.changeFontWindow.accept()

    def about_(self): pass
    def exit_(self):
        sys.exit()
    def checked(self, item, column):
        print( 'emitted!', item.text(column))
        if item.checkState(column) == Qt.Checked:
            item.setBackground(column, QColor(0, 255, 0, 127))
        elif item.checkState(column) == Qt.Unchecked:    
            print("Uncheck ", type(item))
            item.setBackground(0, QColor(255, 0, 0, 127))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())







