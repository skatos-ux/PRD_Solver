from typing import List

from Models.Task import Task


class Technician:
    working_time = 0

    def __init__(self, name, skills: List[Task], availabilities):
        self.name = name
        self.skills = []

        for skill in skills:
            self.skills.append(skill.skills)

        self.skills = list(set(sum(self.skills, [])))
        self.availabilities = availabilities

    def __repr__(self):
        return self.name
