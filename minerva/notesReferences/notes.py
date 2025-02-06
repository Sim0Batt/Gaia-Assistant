import csv
import subprocess


class NoteLink():
    def __init__(self, noteName):
        self.noteName = noteName
        with open('minerva/notesReferences/linkToNotes.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            data = [row for row in csv_reader]
        self.nameLinkDict = data[0]


    def GetLink(self):
        return f"https://www.overleaf.com/project/{self.nameLinkDict[self.noteName]}"
    
    def GetMaterie(self):
        return self.nameLinkDict.keys()
    
    def openRetiLogiche(self):
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "vim /home/simone/appuntiLatex/RetiLogiche.txt"])
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://scenesnap.co/app/education/course/46f5bf86-02da-4357-8ba8-dca0ba9504d2; exit"])

    def openProgAvanzata(self):
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "vim /home/simone/appuntiLatex/ProgAvanzata.txt"])
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://github.com/filippodaniotti/Simulazioni-PrAva/blob/master/Teoria/Riassunto_teoria.pdf; exit"])
