import sqlite3 as sql
import PySimpleGUI as sg

def run(window):
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break


class mainMenu:
    def __init__(self, name):
        self.initItemsDB()
        self.window = sg.Window(title=name, 
                                layout=self.createMainLayout(), 
                                finalize=True, 
                                resizable=True, 
                                margins=(0,0))
        print(self.weaponsTable)

    def initItemsDB(self):
        self.weaponsTable = []
        self.itemsdb = sql.connect("data/items.db")
        self.itemscur = self.itemsdb.cursor()

        for row in self.itemscur.execute("SELECT * FROM weapons ORDER BY name"):
            self.weaponsTable.append(list(row))

    def createMainLayout(self):
        main_tabs = sg.TabGroup(
            layout=[[
                sg.Tab("Characters", self.createCharactersLayout()),
                sg.Tab("Content List", self.createContentLayout()),
                sg.Tab("Information", self.createInformationLayout())
            ]],
            tab_location="topright"
        )
        mainLayout = [[main_tabs]]
        return mainLayout

    def createCharactersLayout(self):
        return [[sg.T("Characters")]]

    def createInformationLayout(self):
        info = '''Small program created by me (Isaac Roberts) for my A-Level Computer Science NEA. 
It acts as a helpful tool for Dungeons and Dragons by giving players access to their  characters, 
items and even monsters all in one place. It even has the functionality to add custom, "homebrew", 
items, feats, classes, subclasses and so much more!'''
        return [[sg.T(info)]]

    def createContentLayout(self):
        content_tabs = sg.TabGroup(
            layout=[[
                sg.Tab("Items", self.createItemsLayout()),
                sg.Tab("Spells", self.createSpellsLayout()),
                sg.Tab("Monsters", self.createMonstersLayout()),
                sg.Tab("Classes", self.createClassesLayout()),
                sg.Tab("Sub-Classes", self.createSubclassesLayout()),
                sg.Tab("Races", self.createRacesLayout()),
                sg.Tab("Sub-Races", self.createSubracesLayout()),
                sg.Tab("Feats", self.createFeatsLayout()),
                sg.Tab("Backgrounds", self.createBackgroundsLayout()),
                sg.Tab("Languages", self.createLanguagesLayout()),
                sg.Tab("Selections", self.createSelectionsLayout()),
                sg.Tab("Pact Boons", self.createBoonsLayout()),
                sg.Tab("Eldritch Invocations", self.createInvocationsLayout())
            ]]
        )
        return [[content_tabs]]

    def createItemsLayout(self):
        weapons_tab = [
            [
                sg.Table(self.weaponsTable,
                        headings=['Name','Cost','Damage','Ranged','Type','Magic','Max Range','Min Range'],
                        key='-WEAPONS_TABLE-')
            ]
        ]
        items_tabs = sg.TabGroup(
            layout=[[
                sg.Tab("Weapons", weapons_tab)
            ]]
        )
        return [[items_tabs]]
    def createSpellsLayout(self):
        return [[sg.T("Spells coming soon..")]]
    def createMonstersLayout(self):
        return [[sg.T("Monsters coming soon..")]]
    def createClassesLayout(self):
        return [[sg.T("Classes coming soon..")]]
    def createSubclassesLayout(self):
        return [[sg.T("Sub-Classes coming soon..")]]
    def createRacesLayout(self):
        return [[sg.T("Classes coming soon..")]]
    def createSubracesLayout(self):
        return [[sg.T("Sub-Races coming soon..")]]
    def createFeatsLayout(self):
        return [[sg.T("Feats coming soon..")]]
    def createBackgroundsLayout(self):
        return [[sg.T("Backgrounds coming soon")]]
    def createLanguagesLayout(self):
        return [[sg.T("Languages coming soon..")]]
    def createSelectionsLayout(Self):
        return [[sg.T("Selections coming soon..")]]
    def createBoonsLayout(self):
        return [[sg.T("Boons coming soon..")]]
    def createInvocationsLayout(self):
        return [[sg.T("Invocations coming soon..")]]

if __name__ == "__main__":
    main_menu = mainMenu("Test")
    window = main_menu.window
    run(window)
    window.close()
