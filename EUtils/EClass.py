import json
import os
import requests
from typing import Self
from .EWidgets import (
  EHSeperator, ECollapsibleBox, EVSeperator,
  EWrapLabel
)
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QTabWidget, QHBoxLayout, QFrame, 
    QScrollArea, QPushButton, QMainWindow,
    QLineEdit, QPlainTextEdit
)
from PySide6.QtCore import Qt, QSize, QKeyCombination
from PySide6.QtGui import QPixmap, QFont

API_URI = "https://www.dnd5eapi.co/graphql/"
def run_query(uri, query, statusCode, headers=None):
    request = requests.post(uri, json={'query': query})
    if request.status_code == statusCode:
        return request.json()
    else:
        raise Exception(f"Unexpected status code returned: {request.status_code}")
getClasses = '''
query Query {
  classes {
    name
    index
    hit_die
    saving_throws {
      index
      full_name
    }
    multi_classing {
      prerequisites {
        ability_score {
          index
        }
        minimum_score
      }
      prerequisite_options {
        type
        from {
          option_set_type
          options {
            option_type
            minimum_score
            ability_score {
              index
            }
          }
        }
      }
    }
    proficiencies {
      index
      type
    }
    proficiency_choices {
      choose
      desc
      from {
        options {
          ... on ProficiencyChoiceOption {
            option_type
            choice {
              choose
            }
          }
          ... on ProficiencyReferenceOption {
            option_type
            item {
              name
              index
            }
          }
        }
      }
    }
  }
}
'''

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
        dnd_classes = run_query(API_URI,getClasses,200)["data"]["classes"]
        for dnd_class in dnd_classes:
            widget = EClassWidget(dnd_class)
            self.classScrollLayout.addWidget(ECollapsibleBox(widget.name, widget, False))


class EClassWidget(QWidget):
    def __init__(self, information: dict) -> None:
        super(EClassWidget, self).__init__()
        lay = QVBoxLayout(self)
        line1 = QHBoxLayout()
        line2 = QHBoxLayout()
        line3 = QHBoxLayout()
        line4 = QHBoxLayout()

        self.information = information
        keys = self.information.keys()
        self.name = self.information["name"] if "name" in keys else ""
        self.index = self.information["index"] if "index" in keys else None
        self.hit_die = self.information["hit_die"] if "hit_die" in keys else None
        throws = self.information["saving_throws"] if "saving_throws" in keys else None
        self.saving_throws_indexes = [throw["index"] for throw in throws] if throws else None
        self.saving_throws_names = [throw["full_name"] for throw in throws] if throws else None
        self.proficiency_choices = self.information["proficiency_choices"][0]["choose"] if "proficiency_choices" in keys else None
        options = self.information["proficiency_choices"][0]["from"]["options"] if "proficiency_choices" in keys else None
        self.proficiency_choices_from_indexes = [option["item"]["index"] for option in options] if options else None
        self.proficiency_choices_from_names = [option["item"]["name"] for option in options] if options else None
        self.proficiencies = [profs["index"] for profs in self.information["proficiencies"]] if self.information["proficiencies"] else None

        line1.addWidget(EWrapLabel(f"Name: {self.name}"))
        line1.addWidget(EWrapLabel(f"Index: {self.index}"))
        line2.addWidget(EWrapLabel(f"Hit Die: d{self.hit_die}"))
        line2.addWidget(EWrapLabel(f"Saving Throws: {self.saving_throws_names}"))
        line3.addWidget(EWrapLabel(f"Proficiency Choices: {self.proficiency_choices}"))
        line3.addWidget(EWrapLabel(f"Proficiency Options: {self.proficiency_choices_from_names}"))
        line4.addWidget(EWrapLabel(f"Proficiencies: {self.proficiencies}"))

        lay.addLayout(line1)
        lay.addWidget(EHSeperator())
        lay.addLayout(line2)
        lay.addWidget(EHSeperator())
        lay.addLayout(line3)
        lay.addWidget(EHSeperator())
        lay.addLayout(line4)


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

    def togglePreview(self) -> None:
        vis = self.preview.isVisible()
        self.preview.setVisible(not vis)
        self.previewButton.setIcon(self.previewFalse) if vis is True else self.previewButton.setIcon(self.previewTrue)
