from PySide6.QtCore import QRect
from PySide6.QtGui import QPalette, QColor, QPixmap
from PySide6.QtWidgets import QWidget, QFrame, QStackedLayout, QHBoxLayout, QLabel

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

class __ECollapsibleHeader(QWidget):
    def __init__(self, name, content):
        super(__ECollapsibleHeader, self).__init__()
        self.content = content
        self.expandIcon = QPixmap(":teDownArrow.png")
        self.collapseIcon = QPixmap(":teRightArrow.png")

        stack = QStackedLayout(self)
        stack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        widget = QWidget()
        lay = QHBoxLayout(widget)

        self.icon = QLabel()
        self.icon.setPixmap(self.expandIcon)

class ECollapsible(QWidget):
    def __init__(self):
        super(ECollapsible, self).__init__()

