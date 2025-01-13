class todo():
    def __init__(self, id, task):
        self.id = id
        self.task = task

    def __str__(self):
        return f"{self.id} - {self.task}"
    