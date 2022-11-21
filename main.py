class item:
    def __init__(self) -> None:
        pass
from role import role

classes = []
fighter = role._JSONToClass("data/classes/fighter.json")
print(fighter)