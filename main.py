import logging
import os

from EClass import EClassWidget, EClassesWidget, EClassesTabWidget
from EUtils import EColor

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import ( 
    QApplication, QMainWindow, QWidget,
    QTabWidget, QToolBar, QStatusBar,
    QLabel, QVBoxLayout, QBoxLayout
)

logging.basicConfig(filename="latest.log",format='%(asctime)s - %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')

class MainWindow(QMainWindow):
    def __init__(self):
        logging.info("MainWindow init START")
        super(MainWindow, self).__init__()

        self.setWindowTitle("ExtraDND")
        self.setMinimumSize(QSize(604,200))

        tabs = QTabWidget()
        tabs.addTab(self._characterTab(), "Characters")
        tabs.addTab(self._contentTab(), "Content List")
        tabs.addTab(self._informationTab(), "Information")

        self.setCentralWidget(tabs)

        import_button = QAction(QIcon("icons/arrow.png"), "&Import", self)
        import_button.setStatusTip("Import custom content and characters!")
        export_button = QAction(QIcon("icons/arrow-180.png"), "&Export", self)
        export_button.setStatusTip("Export custom content and characters!")

        menu = self.menuBar()
        file = menu.addMenu("&File")
        file.addAction(import_button)
        file.addAction(export_button)

        logging.info("MainWindow init FINISH")

    def _characterTab(self) -> QWidget:
        return QWidget()

    def _contentTab(self) -> QTabWidget:
        tabs = QTabWidget()
        tabs.addTab(QWidget(), "Items")
        tabs.addTab(QWidget(), "Spells")
        tabs.addTab(QWidget(), "Monsters")
        tabs.addTab(EClassesTabWidget(), "Classes")
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