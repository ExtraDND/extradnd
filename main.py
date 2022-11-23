import logging
import os

from EClass import EClassWidget, EClassesWidget
from EUtils import EColor

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import ( 
    QApplication, QMainWindow, QWidget,
    QTabWidget, QToolBar, QStatusBar,
    QLabel, QVBoxLayout, QBoxLayout
)

logging.basicConfig(filename="latest.log",format='%(levelname)s:%(message)s', level=logging.DEBUG)

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

    def __classesTab(self) -> QTabWidget:
        tabs = QTabWidget()
        tabs.addTab(EClassesWidget(), "Classes")
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