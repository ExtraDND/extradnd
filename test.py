import requests
import json
from typing import Self

API_URL = "https://www.dnd5eapi.co/graphql/"
# response = requests.get(f"{API_URL}")
# response = requests.request(method="POST", url="https://www.dnd5eapi.co/graphql/classes/", json={"query":query})
# print(response)


class EClassWidget:
    def __init__(self, information: dict) -> None:
        self.information = information
        keys = self.information.keys()
        self.name = self.information["name"] if "name" in keys else None
        self.index = self.information["index"] if "index" in keys else None
        self.hit_die = self.information["hit_die"] if "hit_die" in keys else None
        throws = self.information["saving_throws"] if "saving_throws" in keys else None
        self.saving_throws_indexes = [throw["index"] for throw in throws] if throws else None
        self.saving_throws_names = [throw["full_name"] for throw in throws] if throws else None
        self.proficiency_choices = self.information["proficiency_choices"][0]["choose"] if "proficiency_choices" in keys else None
        options = self.information["proficiency_choices"][0]["from"]["options"] if "proficiency_choices" in keys else None
        self.proficiency_choices_from_indexes = [option["item"]["index"] for option in options] if options else None
        self.proficiency_choices_from_names = [option["item"]["name"] for option in options] if options else None
        # self.subclass = information["subclass"]
        # self.subclass_level = information["subclass_level"]
        # self.spellcasting = information["spellcasting"]
        # self.skill_expertise = information["skill_expertise"]
        # self.skill_expertise_choices = information["skill_expertise_choices"]
        # self.modifiers = information["modifiers"]
        # self.starting_equipment = information["starting_equipment"]
        # self.features = information["features"]
    
    def _getClassInfo(self) -> str:
        info = f"""
Name: {self.name} | Index: {self.index}
===================================================
Hit Die: d{self.hit_die} | Spellcaster: NULL
Saving Throws: {self.saving_throws_names}
===================================================
Proficiency Choices: {self.proficiency_choices}
Proficiency Options: {self.proficiency_choices_from_names}
===================================================
Expertise Choices: NULL
Expertice Options: NULL
===================================================
Subclass: NULL
Subclass Level: NULL
===================================================
Modifiers: NULL
Starting Equipment: NULL
Features: NULL
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

def run_query(uri, query, statusCode, headers=None):
    request = requests.post(uri, json={'query': query})
    if request.status_code == statusCode:
        return request.json()
    else:
        raise Exception(f"Unexpected status code returned: {request.status_code}")

query = '''
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

for i in run_query(API_URL,query,200)["data"]["classes"]:
    print(EClassWidget(i))