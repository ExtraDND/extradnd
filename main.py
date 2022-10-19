class role:
    def __init__(self, information):
        self.name = information["name"]
        self.source = information["source"]
        self.description = information["description"]
        self.hit_die = information["hit_die"]
        self.subclass = information["subclass"]
        self.subclass_level = information["subclass_choice"]
        self.saving_throws = information["saving_throws"]
        self.spellcasting = information["spellcasting"]
        self.skill_proficiency = information["skill_proficiencies"]
        self.skill_proficiency_choices = information["skill_proficiencies_choices"]
        self.skill_expertise = information["skill_proficiencies"]
        self.skill_expertise_choices = information["skill_proficiencies_choices"]
        self.modifiers = information["modifiers"]
        self.starting_equipment = information["starting_equipment"]
        self.features = information["features"]
    