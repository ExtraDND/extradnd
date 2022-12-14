import json
import os
from typing import Self
from .EWidgets import EHSeperator, ECollapsibleBox, EVSeperator
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QTabWidget, QHBoxLayout, QFrame, 
    QScrollArea, QPushButton, QMainWindow,
    QLineEdit, QPlainTextEdit
)
from PySide6.QtCore import Qt, QSize, QKeyCombination
from PySide6.QtGui import QPixmap, QFont

class EClassesTabWidget(QTabWidget):
    def __init__(self) -> None:
        super(EClassesTabWidget, self).__init__()
        self.addTab(EClassesWidget(), "Classes")
        self.addTab(QWidget(), "Subclasses")


class EClassesWidget(QWidget):
    def __init__(self) -> None:
        super(EClassesWidget, self).__init__()

        self.classWindow = None

        self.classScroll = QScrollArea()
        self.classScrollLayout = QVBoxLayout()
        lay = QVBoxLayout()
        lay.setContentsMargins(0,4,0,0)

        self.classScrollLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.classScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.classScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.classScroll.setWidgetResizable(True)

        classButtons = QHBoxLayout()
        classButtons.setAlignment(Qt.AlignmentFlag.AlignRight)
        classButtons.setContentsMargins(0,0,4,0)

        newClassIco = QPixmap("icons/book--plus.png")
        newClass = QPushButton()
        newClass.setIcon(newClassIco)
        newClass.setFixedSize(newClassIco.size() + QSize(8,8))
        newClass.clicked.connect(self.openClassCreator)
        classButtons.addWidget(newClass)

        delClassIco = QPixmap("icons/book--minus.png")
        delClass = QPushButton()
        delClass.setIcon(delClassIco)
        delClass.setFixedSize(delClassIco.size() + QSize(8,8))
        classButtons.addWidget(delClass)

        editClassIco = QPixmap("icons/book--pencil.png")
        editClass = QPushButton()
        editClass.setIcon(editClassIco)
        editClass.setFixedSize(editClassIco.size() + QSize(8,8))
        classButtons.addWidget(editClass)

        self._startClassList()
        
        widget = QWidget()
        widget.setLayout(self.classScrollLayout)
        self.classScroll.setWidget(widget)
        lay.addLayout(classButtons)
        lay.addWidget(self.classScroll)
        self.setLayout(lay)

    def openClassCreator(self) -> None:
        if self.classWindow == None: self.classWindow = EClassCreatorWindow()
        self.classWindow.show()
        

    def _startClassList(self) -> None:
        class_files = os.listdir("data/classes")
        for f in class_files:
            role = EClassWidget._JSONToClass(f"data/classes/{f}")
            self.classScrollLayout.addWidget(ECollapsibleBox(role.name, role, False))


class EClassWidget(QWidget):
    def __init__(self, information: dict) -> None:
        super(EClassWidget, self).__init__()
        lay = QVBoxLayout(self)
        line1 = QHBoxLayout()
        line2 = QVBoxLayout()
        line3 = QHBoxLayout()
        line4 = QHBoxLayout()
        line5 = QHBoxLayout()
        self.name = information["name"]
        self.source = information["source"]
        line1.addWidget(QLabel(f"Name: {self.name}"))
        line1.addWidget(QLabel(f"Source: {self.source}"))
        self.description = information["description"]
        desc = QLabel(self.description)
        desc.setWordWrap(True)
        line2.addWidget(QLabel("Description:"))
        line2.addWidget(desc)
        self.hit_die = information["hit_die"]
        self.saving_throws = information["saving_throws"]
        line3.addWidget(QLabel(f"Hit Die: d{self.hit_die}"))
        line3.addWidget(QLabel(f"Saving Throws: {self.__getSavingThrowStr(self.saving_throws)}"))
        self.subclass = information["subclass"]
        self.subclass_level = information["subclass_level"]
        line4.addWidget(QLabel(f"Subclass: {self.__convertName(self.subclass)}"))
        line4.addWidget(QLabel(f"Subclass Level: {self.subclass_level}"))
        self.spellcasting = information["spellcasting"]
        self.skill_proficiency = information["skill_proficiency"]
        self.skill_proficiency_choices = information["skill_proficiency_choices"]
        line5.addWidget(QLabel(f"{self.skill_proficiency}"))
        line5.addWidget(QLabel(f"{self.skill_proficiency_choices}"))
        self.skill_expertise = information["skill_expertise"]
        self.skill_expertise_choices = information["skill_expertise_choices"]
        self.modifiers = information["modifiers"]
        self.starting_equipment = information["starting_equipment"]
        self.features = information["features"]

        lay.addLayout(line1)
        lay.addWidget(EHSeperator())
        lay.addLayout(line2)
        lay.addWidget(EHSeperator())
        lay.addLayout(line3)
        lay.addWidget(EHSeperator())
        lay.addLayout(line4)
        lay.addWidget(EHSeperator())
        lay.addLayout(line5)
    
    def _getClassInfo(self) -> str:
        info = f"""
Name: {self.name} | Source: {self.source}
===================================================
Hit Die: d{self.hit_die} | Spellcaster: {self.spellcasting}
Saving Throws: {self.saving_throws}
===================================================
Proficiency Choices: {self.skill_proficiency}
Proficiency Options: {self.skill_proficiency_choices}
===================================================
Expertise Choices: {self.skill_expertise}
Expertice Options: {self.skill_expertise_choices}
===================================================
Subclass: {self.subclass}
Subclass Level: {self.subclass_level}
===================================================
Modifiers: {self.modifiers}
Starting Equipment: {self.starting_equipment}
Features: {self.features}
"""
        return info

    @staticmethod
    def __convertName(name: str) -> str:
        result = ""
        nameSpl = name.split("_")
        for word in nameSpl:
            result += f"{word.capitalize()} "
        return result

    @staticmethod
    def __getSavingThrowStr(svTrs: list[str]) -> str:
        result = ""
        if "str" in svTrs: result += "Strength, "
        if "dex" in svTrs: result += "Dexterity, "
        if "con" in svTrs: result += "Constitution, "
        if "int" in svTrs: result += "Intelligence, "
        if "wis" in svTrs: result += "Wisdom, "
        if "cha" in svTrs: result += "Charisma, "
        result = result[:-2]
        return result

    @staticmethod
    def __getJSONfileName(name: str) -> str:
        new_name = ""
        for character in name:
            if character != " ":
                new_name += character
            else:
                new_name += "_"
        return new_name.lower() + ".json"

    @staticmethod
    def _JSONToClass(class_file: str) -> Self:
        with open(class_file, "r") as json_f:
            data = json.load(json_f)
            return EClassWidget(data)

    @staticmethod
    def _ClassToJSON(data: dict) -> str:
        with open("data/classes/"+EClassWidget.__getJSONfileName(data["name"]), "w+") as json_f:
            json_data = json.dumps(data)
            json_f.write(json.dumps(data))
            return json_data

    def __str__(self) -> str:
        return self._getClassInfo()


class EClassCreatorWindow(QMainWindow):
    def __init__(self) -> None:
        super(EClassCreatorWindow, self).__init__()
        self.setWindowTitle("Class Creator")
        winIcon = QPixmap("icons/book--plus.png")
        self.setWindowIcon(winIcon)

        lay = QHBoxLayout()
        editor = QVBoxLayout()
        previewLay = QHBoxLayout()
        self.preview = QWidget()
        self.preview.setLayout(previewLay)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        lay.addLayout(editor)
        lay.addWidget(self.preview)
        previewLay.addWidget(EVSeperator())
        previewLay.addWidget(QLabel("Preview"))
        self.preview.setVisible(False)

        line1 = QHBoxLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("Class Name *")
        self.source = QLineEdit()
        self.source.setPlaceholderText("Source Name *")
        line1.addWidget(self.name)
        line1.addWidget(self.source)

        line2 = QHBoxLayout()
        self.description = QPlainTextEdit()
        self.description.setPlaceholderText("Description...")
        # h = 3 * self.description.font()
        # self.description.setFixedHeight()
        line2.addWidget(self.description)

        editor.addLayout(line1)
        editor.addLayout(line2)
        
        self.previewTrue = QPixmap("icons/book-open.png")
        self.previewFalse = QPixmap("icons/book-brown.png")
        self.previewButton = QPushButton()
        self.previewButton.setCheckable(True)
        self.previewButton.clicked.connect(self.togglePreview)
        self.previewButton.setText("Preview")
        self.previewButton.setIcon(self.previewFalse)
        editor.addWidget(self.previewButton)

        widget = QWidget()
        widget.setLayout(lay)
        self.setCentralWidget(widget)

    def togglePreview(self):
        vis = self.preview.isVisible()
        self.preview.setVisible(not vis)
        self.previewButton.setIcon(self.previewFalse) if vis is True else self.previewButton.setIcon(self.previewTrue)
