from PySide6 import QtCore
from PySide6.QtCore import Qt, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation, QSize
from PySide6.QtGui import QPalette, QColor, QFont, QPixmap
from PySide6.QtWidgets import ( 
    QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QWidget, QFrame, QToolButton,
    QScrollArea, QSizePolicy, QVBoxLayout,
    QMainWindow, QApplication
)
from EUtils import EHSeperator


class CollapsibleBox(QWidget):
    def __init__(self, name, content):
        super(CollapsibleBox, self).__init__()
        self.header = QLabel(name)
        collapseIcon = QPixmap(":teRightArrow.png")
        expandIcon = QPixmap(":teDownArrow.png")

        headerFont = QFont()
        headerFont.setBold(True)
        headerFont.setCapitalization(QFont.Capitalization.Capitalize)
        self.header.setFont(headerFont)
        self.header.setPixmap(expandIcon)

        lay = QVBoxLayout(self)

        lay.addWidget(EHSeperator())
        lay.addWidget(self.header)
        lay.addWidget(content)
        lay.addWidget(EHSeperator())

        self.setLayout(lay)



class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        collapse = CollapsibleBox("Collapse", QLabel("Content"))

        verticalLayout = QVBoxLayout(self)
        verticalLayout.addWidget(QLabel("Test 1"))
        verticalLayout.addWidget(collapse)
        verticalLayout.addWidget(QLabel("Test 2"))

        self.setLayout(verticalLayout)

        self.setWindowTitle("Collapse Test")
        self.show()

if __name__ == '__main__':
    app = QApplication()
    ex = Example()
    app.exec()