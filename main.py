import json

class item:
    def __init__(self) -> None:
        pass

class role:
    def __init__(self, information: dict) -> None:
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
    
    def classInfo(self) -> str:
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
    def __JSONfileName(name: str) -> str:
        new_name = ""
        for character in name:
            if character != " ":
                new_name += character
            else:
                new_name += "_"
        return new_name.lower() + ".json"

    @staticmethod
    def _JSONToClass(class_file: str) -> dict:
        with open(class_file, "r") as json_f:
            data = json.load(json_f)
            return role(data)

    @staticmethod
    def _ClassToJSON(data: dict) -> str:
        with open("data/classes/"+role.__JSONfileName(data["name"]), "w+") as json_f:
            json_data = json.dumps(data)
            json_f.write(json.dumps(data))
            return json_data

classes = []
fighter = role._JSONToClass("data/classes/fighter.json")
fighter2 = fighter
fighter2["name"] = "fighter2"
print(type(role._ClassToJSON(fighter2)))