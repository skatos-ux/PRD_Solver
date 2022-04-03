import numpy as np
from typing import List

from Models.Client import Client
from Models.ClientOptions import ClientOptions
from Models.Task import Task
from Models.Technician import Technician


class Company:
    technicians = []
    clients = []
    machines = []

    c_planning = [
        [
            [[], [], 0],  # Period 1 : Des techniciens, un client, une tâche
            [[], [], 0],  # Period 2
            [[], [], 0],  # Period 3
            [[], [], 0],  # Period 4
            [[], [], 0],  # Period 5
            [[], [], 0],  # Period 6
            [[], [], 0],  # Period 7
            [[], [], 0],  # Period 8
        ] for _ in range(7)
    ]  # 7 Jours

    def __init__(self, technicians):
        self.technicians = technicians

    def find_technicians_by_skills(self, _skills_required):
        c_technicians = []
        for technician in self.technicians:
            if np.array_equal(intersection(technician.skills, _skills_required), _skills_required):
                c_technicians.append(technician)
        return c_technicians

    def find_quickest_for_technicians(self, _technicians, _start, _duration):

        p_technicians = []
        c_period = -1
        day_number = -1

        for day_number, day in enumerate(self.c_planning):
            for index, period in enumerate(day):
                # On ne marche pas sur les horaires des autres
                if period[0] or index < _start:
                    continue
                # On supprime l'intersection, on veut les techniciens qui ne travaillent pas
                p_technicians = not_intersection(_technicians, list(period[0]))
                # On sauvegarde la periode
                c_period = index
                # On enlève les techniciens qui ne travaillent pas durant cette periode
                p_technicians = [technician for technician in p_technicians if technician.availabilities[0] <= c_period and c_period + _duration < technician.availabilities[1]]
                # On regarde si on ne dépasse pas la journée
                if c_period + _duration <= len(self.c_planning[day_number]):
                    # On regarde si le technicien n'est pas pris par la suite
                    for next_period in self.c_planning[day_number][index: index + _duration]:
                        p_technicians = not_intersection(p_technicians, list(next_period[0]))
                        if not p_technicians:
                            c_period = -1
                            break
                        else:
                            return p_technicians, day_number, c_period
                else:
                    break
        if c_period == -1:
            raise Exception("TECHNICIAN ERROR : NO DISPONIBILITY")

        return p_technicians, day_number, c_period

    def try_to_schedule(self, _client: Client, _tests: List[Task], _duration):

        if _client.availabilities[1] - _client.availabilities[0] < _duration:
            # Le temps de disponibilité du client est inférieur au temps de tests
            raise Exception(f'DURATION ERROR : {_client}')

        # On récupère les skills nécéssaires
        c_skills = []
        for test in _tests:
            c_skills.append(test.skills)

        p_technicians = self.find_technicians_by_skills(list(set(sum(c_skills, []))))
        # Si aucuns techniciens n'a les skills
        if not p_technicians:
            raise Exception('SKILL ERROR : NO TECHNICIAN')
        # Techniciens ayant les skills nécessaires et qui pourraient commencer le plus tôt
        p_technicians, day_number, c_period = self.find_quickest_for_technicians(p_technicians,
                                                                                 _client.availabilities[0],
                                                                                 _duration)
        # On veut faire travailler celui qui a le moins travailler
        technician = get_min_wt(p_technicians)

        return technician, day_number, c_period

    def planning(self, _clients_options: List[ClientOptions]):
        c_clients_options = sorted(_clients_options, key=lambda co: co.client.availabilities[0])
        for client_option in c_clients_options:
            for redo in range(client_option.redo):
                client = client_option.client
                duration = calc_duration(client.tasks)
                c_technician, day_number, c_period = self.try_to_schedule(client, client.tasks, duration)
                c_technician.working_time += duration
                for index, periods in enumerate(range(c_period, c_period + duration)):
                    self.c_planning[day_number][periods][0].append(c_technician)
                    self.c_planning[day_number][periods][1].append(client)
                    self.c_planning[day_number][periods][2] = client.tasks[index].name

    def planning_reset(self):
        self.c_planning = [
            [
                [[], [], 0],  # Period 1 : Des techniciens, un client, une tâche
                [[], [], 0],  # Period 2
                [[], [], 0],  # Period 3
                [[], [], 0],  # Period 4
                [[], [], 0],  # Period 5
                [[], [], 0],  # Period 6
                [[], [], 0],  # Period 7
                [[], [], 0],  # Period 8
            ] for _ in range(7)
        ]

    def planning_print(self):
        for index, day in enumerate(self.c_planning):
            print(f"DAY{index}:")
            for period in day:
                print(period)
            print()


def not_intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value not in lst2]
    lst4 = [value for value in lst2 if value not in lst1]
    return lst3 + lst4


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def get_min_wt(_technicians: List[Technician]):
    return sorted(_technicians, key=lambda technician: technician.working_time)[0]


def calc_duration(_tasks: List[Task]):
    duration = 0
    for task in _tasks:
        duration += task.duration
    return duration


if __name__ == "__main__":
    t1 = Task("pneu", [1], 1)
    t2 = Task("vitres", [1, 2], 1)
    t3 = Task("complet", [1, 2, 3], 1)

    joe = Technician("joe", [t1, t3], [0, 8])
    jack = Technician("jack", [t2], [0, 8])
    jey = Technician("jey", [t3], [0, 8])

    peugeot = Client("Peugeot", [t1, t2, t3], [1, 8])
    ferrari = Client("Ferari", [t3], [0, 8])

    co1 = ClientOptions(peugeot, 6)
    co2 = ClientOptions(ferrari, 12)

    company = Company([joe, jack, jey])

    company.planning([co1, co2])
    company.planning_print()
