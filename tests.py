import unittest

from Models.Client import Client
from Models.ClientOptions import ClientOptions
from Models.Task import Task
from Models.Technician import Technician
from solver import Company, calc_duration, get_min_wt, intersection, not_intersection


class SolverTests(unittest.TestCase):

    def setUp(self):

        self.t1 = Task("pneu", [1], 1)
        self.t2 = Task("vitres", [1, 2], 1)
        self.t3 = Task("complet", [1, 2, 3], 1)

        self.joe = Technician("joe", [self.t1, self.t3], [0, 8])
        self.jack = Technician("jack", [self.t2], [0, 8])
        self.jey = Technician("jey", [self.t3], [1, 8])

        self.peugeot = Client("Peugeot", [self.t1, self.t2, self.t3], [1, 8])
        self.ferrari = Client("Ferari", [self.t3], [0, 8])

        self.co1 = ClientOptions(self.peugeot, 1)
        self.co2 = ClientOptions(self.ferrari, 1)

        self.joe.working_time = 0
        self.jey.working_time = 0
        self.jack.working_time = 0

        self.company = Company([self.joe, self.jack, self.jey])
        self.company.planning_reset()

        self.company.planning([self.co1, self.co2])

    def test_calc_duration_ok(self):
        """
        Test that the sum of a list of task's duration is right
        """
        duration = calc_duration([self.t1, self.t2, self.t3])
        self.assertEqual(duration, 3)

    def test_get_min_wt_ok(self):
        """
        Test that the function returns the technician with the lowest working_time
        """
        pierre = Technician("pierre", [self.t1, self.t3], [0, 8])
        henry = Technician("henry", [self.t1, self.t3], [0, 8])
        mathieu = Technician("mathieu", [self.t1, self.t3], [0, 8])

        pierre.working_time = 1
        henry.working_time = 2
        mathieu.working_time = 3

        technician = get_min_wt([mathieu, henry, pierre])
        self.assertEqual(technician, pierre)

        pierre.working_time = 2
        technician = get_min_wt([mathieu, henry, pierre])
        self.assertEqual(technician, henry)

    def test_intersection_ok(self):
        """
        Test that the function returns the real intersection of arrays
        """
        list1 = [1, 2, 3]
        list2 = [2, 3, 4]
        self.assertEqual(intersection(list1, list2), [2, 3])

    def test_not_intersection_ok(self):
        """
        Test that the function returns the elements outside of the intersection of the arrays
        """
        list1 = [1, 2, 3]
        list2 = [2, 3, 4]
        self.assertEqual(not_intersection(list1, list2), [1, 4])

    def test_company_try_to_schedule(self):
        """
        Test that the function returns the rights values (quickest technician, quickest day number, correct duration)
        """
        c_technician, day_number, c_period = self.company.try_to_schedule(self.peugeot, self.peugeot.tasks, 2)
        self.assertEqual(c_technician, self.joe)
        self.assertEqual(day_number, 0)
        self.assertEqual(c_period, 4)

    def test_company_find_quickest_for_technician(self):
        """
        Test that the function returns the rights values (quickest technician, quickest day number, correct duration)
        """
        p_technicians, day_number, c_period = self.company.find_quickest_for_technicians(
            [self.jey, self.joe],
            self.peugeot.availabilities[0],
            1)
        self.assertEqual(p_technicians, [self.jey, self.joe])
        self.assertEqual(day_number, 0)
        self.assertEqual(c_period, 4)

    def test_company_find_technicians_by_skills(self):
        """
        Test that the function returns the rights values (technician with according skill sets)
        """
        p_technicians = self.company.find_technicians_by_skills([1, 2, 3])
        self.assertEqual(p_technicians, [self.joe, self.jey])


if __name__ == '__main__':
    unittest.main()
