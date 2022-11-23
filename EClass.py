import json
import os
from EUtils import EHSeperator, ECollapsibleBox
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QHBoxLayout, QFrame, QScrollArea

class EClassesTabWidget(QTabWidget):
    def __init__(self):
        super(EClassesTabWidget, self).__init__()
        self.addTab(EClassesWidget(), "Classes")
        self.addTab(QWidget(), "Subclasses")

class EClassesWidget(QScrollArea):
    def __init__(self):
        super(EClassesWidget, self).__init__()
        self.layout = QVBoxLayout()

        class_files = os.listdir("data/classes")
        for f in class_files:
            role = EClassWidget._JSONToClass(f"data/classes/{f}")
            self.layout.addWidget(ECollapsibleBox(role.name, role))
        self.layout.addWidget(QLabel("Test"))
        self.layout.addWidget(QLabel("Test2"))
        self.setLayout(self.layout)

class EClassWidget(QWidget):
    def __init__(self, information: dict) -> None:
        super(EClassWidget, self).__init__()
        self.name = information["name"]
        self.source = information["source"]
        self.description = information["description"]
        self.hit_die = information["hit_die"]
        self.subclass = information["subclass"]
        self.subclass_level = information["subclass_level"]
        self.saving_throws = information["saving_throws"]
        self.spellcasting = information["spellcasting"]
        self.skill_proficiency = information["skill_proficiency"]
        self.skill_proficiency_choices = information["skill_proficiency_choices"]
        self.skill_expertise = information["skill_expertise"]
        self.skill_expertise_choices = information["skill_expertise_choices"]
        self.modifiers = information["modifiers"]
        self.starting_equipment = information["starting_equipment"]
        self.features = information["features"]

        lay = QVBoxLayout(self)
        line1 = QHBoxLayout()
        line1.addWidget(QLabel(f"Name: {self.name}"))
        line1.addWidget(QLabel(f"Source: {self.source}"))
        lay.addLayout(line1)
        lay.addWidget(EHSeperator())
        line2 = QHBoxLayout()
        line2.addWidget(QLabel(f"Hit Die: d{self.hit_die}"))
        lay.addLayout(line2)
        lay.addWidget(EHSeperator())
    
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
    def __getJSONfileName(name: str) -> str:
        new_name = ""
        for character in name:
            if character != " ":
                new_name += character
            else:
                new_name += "_"
        return new_name.lower() + ".json"

    @staticmethod
    def _JSONToClass(class_file: str):
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
