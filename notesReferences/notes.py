import csv


class NoteLink():
    def __init__(self, noteName):
        self.noteName = noteName
        with open('notesReferences/linkToNotes.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            data = [row for row in csv_reader]
        self.nameLinkDict = data[0]


    def GetLink(self):
        return f"https://www.overleaf.com/project/{self.nameLinkDict[self.noteName]}"
    
    def GetMaterie(self):
        return self.nameLinkDict.keys()