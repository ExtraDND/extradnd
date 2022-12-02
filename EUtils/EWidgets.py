from PySide6 import QtCore
from PySide6.QtCore import Qt, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation
from PySide6.QtGui import QPalette, QColor, QPixmap
from PySide6.QtWidgets import (
    QWidget, QFrame, QToolButton,
    QScrollArea, QSizePolicy, QVBoxLayout,
    QPushButton, QLabel
)

class EWrapLabel(QLabel):
    def __init__(self, text: str) -> None:
        super(EWrapLabel, self).__init__(text)
        self.setWordWrap(True)

class EHSeperator(QFrame):
    def __init__(self) -> None:
        super(EHSeperator, self).__init__()
        self.setObjectName("hSeperator")
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        
class EVSeperator(QFrame):
    def __init__(self) -> None:
        super(EVSeperator, self).__init__()
        self.setObjectName("vSeperator")
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

class EColor(QWidget):
    def __init__(self, color: str) -> None:
        super(EColor, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class ECollapsibleBox(QWidget):
    def __init__(self, name: str, content: QWidget, flat: bool=True) -> None:
        super(ECollapsibleBox, self).__init__()
        self.collapseIcon = QPixmap("icons/book-open.png")
        self.expandIcon = QPixmap("icons/book-brown.png")

        self.header = QPushButton()
        self.header.setCheckable(True)
        self.header.setFlat(flat)
        self.header.clicked.connect(self.onClicked)
        self.header.setIcon(self.expandIcon)
        self.header.setText(name)
        self.header.setStyleSheet("QPushButton {font-weight: bold; text-align: left;}")
        self.headerSize = self.header.sizeHint()

        self.content = content
        self.contentSize = self.content.sizeHint()

        lay = QVBoxLayout(self)

        lay.addWidget(self.header)
        lay.addWidget(self.content)
        self.content.setVisible(False)

        self.setLayout(lay)
    
    def onClicked(self) -> None:
        visible = self.content.isVisible()
        self.content.setVisible(not visible)
        self.header.setIcon(self.expandIcon) if visible else self.header.setIcon(self.collapseIcon)
