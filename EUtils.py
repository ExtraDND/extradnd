from PySide6 import QtCore
from PySide6.QtCore import Qt, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QFrame, QToolButton, QScrollArea, QSizePolicy, QVBoxLayout

class EHSeperator(QFrame):
    def __init__(self):
        super(EHSeperator, self).__init__()
        self.setObjectName("hSeperator")
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        
class EVSeperator(QFrame):
    def __init__(self):
        super(EVSeperator, self).__init__()
        self.setObjectName("vSeperator")
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

class EColor(QWidget):
    def __init__(self, color):
        super(EColor, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

