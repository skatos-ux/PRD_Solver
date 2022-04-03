class Task:

    def __init__(self, name, skills, duration):
        self.name = name
        self.skills = skills
        self.duration = duration

    def __repr__(self):
        return repr(self.skills)
