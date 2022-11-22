import logging
import os
from role import Role

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon, QPalette, QColor
from PySide6.QtWidgets import ( 
    QApplication, QMainWindow, QWidget,
    QTabWidget, QToolBar, QStatusBar,
    QLabel
)

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

logging.info("Initialising Colors")
class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
logging.info("Initialised Colors")
# class Frame(QWidget)

logging.info("Initialising Main Window")
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("ExtraDND")
        logging.debug("Set window title")
        self.setMinimumSize(QSize(604,200))
        logging.debug("Set window size")

        tabs = QTabWidget()
        tabs.addTab(self._characterTab(), "Characters")
        tabs.addTab(self._contentTab(), "Content List")
        tabs.addTab(self._informationTab(), "Information")

        self.setCentralWidget(tabs)
        logging.debug("Created main tab group")

        import_button = QAction(QIcon("icons/arrow.png"), "&Import", self)
        import_button.setStatusTip("Import custom content and characters!")
        export_button = QAction(QIcon("icons/arrow-180.png"), "&Export", self)
        export_button.setStatusTip("Export custom content and characters!")
        logging.debug("Created menu actions")

        menu = self.menuBar()
        file = menu.addMenu("&File")
        file.addAction(import_button)
        file.addAction(export_button)
        logging.debug("Created menu bar")

    def __getClasses(self) -> list:
        classes = []
        class_files = os.listdir("data/classes")
        for f in class_files:
            role = Role._JSONToClass(f"data/classes/{f}")
            classes.append(role)
        return classes

    def __classesTab(self) -> QTabWidget:
        tabs = QTabWidget()
        tabs.addTab(self.__getClasses()[0], "Classes")
        tabs.addTab(QWidget(), "Subclasses")
        return tabs

    def _characterTab(self) -> QWidget:
        return QWidget()

    def _contentTab(self) -> QTabWidget:
        tabs = QTabWidget()
        tabs.addTab(QWidget(), "Items")
        tabs.addTab(QWidget(), "Spells")
        tabs.addTab(QWidget(), "Monsters")
        tabs.addTab(self.__classesTab(), "Classes")
        tabs.addTab(QWidget(), "Races")
        tabs.addTab(QWidget(), "Feats")
        tabs.addTab(QWidget(), "Backgrounds")
        tabs.addTab(QWidget(), "Languages")
        tabs.addTab(QWidget(), "Selections")
        logging.debug("Created content list tab group")
        return tabs

    def _informationTab(self) -> QWidget:
        return QWidget()


app = QApplication()

window = MainWindow()
window.show()
logging.info("Create Main Window instance")
logging.info("Start execution loop")

app.exec()