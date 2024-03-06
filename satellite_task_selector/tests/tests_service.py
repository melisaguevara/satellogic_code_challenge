from django.test import SimpleTestCase

from ..services import TasksService


class TasksServiceTests(SimpleTestCase):
    def setUp(self):
        self.service = TasksService()
        return super().setUp()

    def test_get_executable_tasks_with_empty_list_as_input(self):
        executable_tasks = self.service.get_most_profitable_subset_of_tasks([
        ])
        self.assertEqual(executable_tasks.tasks, [])

    def test_get_profitable_tasks_with_no_incompatible_items_exponential_algorithm(self):
        input_tasks = [
            {
                "name": "upgrade to v2.1",
                "resources": ['proc'],
                "profit": 2.3
            },
            {
                "name": "run healthcheck",
                "resources": [],
                "profit": 0.4
            },
            {
                "name": "capture for client 1509",
                "resources": [
                    "disk",
                    "cam"
                ],
                "profit": 5
            },
        ]
        expected_result = [
            {
                "name": "upgrade to v2.1",
                "resources": ['proc'],
                "profit": 2.3
            },
            {
                "name": "run healthcheck",
                "resources": [],
                "profit": 0.4
            },
            {
                "name": "capture for client 1509",
                "resources": [
                    "disk",
                    "cam"
                ],
                "profit": 5
            },
        ]
        executable_tasks = self.service.find_most_profitable_subset_among_all_compatible_subsets(
            input_tasks)
        self.assertEqual(executable_tasks.tasks, expected_result)

    def test_get_executable_tasks_with_incompatible_items_exponential_algorithm(self):
        input_tasks = [
            {
                "name": "upgrade to v2.1",
                "resources": ['proc'],
                "profit": 2.3
            },
            {
                "name": "clean disk",
                "resources": ['disk'],
                "profit": 0.4
            },
            {
                "name": "capture for client 1509",
                "resources": [
                    "disk",
                    "cam"
                ],
                "profit": 5
            },
        ]
        expected_result = [
            {
                "name": "upgrade to v2.1",
                "resources": ['proc'],
                "profit": 2.3
            },
            {
                "name": "capture for client 1509",
                "resources": [
                    "disk",
                    "cam"
                ],
                "profit": 5
            },
        ]
        executable_tasks = self.service.find_most_profitable_subset_among_all_compatible_subsets(
            input_tasks)
        self.assertEqual(executable_tasks.tasks, expected_result)

    def test_get_profitable_tasks_with_no_incompatible_items_quadratic_algorithm(self):
        input_tasks = [
            {
                "name": "upgrade to v2.1",
                "resources": ['proc'],
                "profit": 2.3
            },
            {
                "name": "run healthcheck",
                "resources": [],
                "profit": 0.4
            },
            {
                "name": "capture for client 1509",
                "resources": [
                    "disk",
                    "cam"
                ],
                "profit": 5
            },
        ]
        expected_result = [
            {
                "name": "capture for client 1509",
                "resources": [
                    "disk",
                    "cam"
                ],
                "profit": 5
            },
            {
                "name": "upgrade to v2.1",
                "resources": ['proc'],
                "profit": 2.3
            },
            {
                "name": "run healthcheck",
                "resources": [],
                "profit": 0.4
            },
        ]
        executable_tasks = self.service.find_most_profitable_subset_among_some_compatible_subsets(
            input_tasks)
        self.assertEqual(executable_tasks.tasks, expected_result)

    def test_get_executable_tasks_with_incompatible_items_quadratic_algorithm(self):
        input_tasks = [
            {
                "name": "capture for client 1509",
                "resources": [
                    "disk",
                    "cam"
                ],
                "profit": 5
            },
            {
                "name": "upgrade to v2.1",
                "resources": ['proc'],
                "profit": 2.3
            },
            {
                "name": "clean disk",
                "resources": ['disk'],
                "profit": 0.4
            },
        ]
        expected_result = [
            {
                "name": "capture for client 1509",
                "resources": [
                    "disk",
                    "cam"
                ],
                "profit": 5
            },
            {
                "name": "upgrade to v2.1",
                "resources": ['proc'],
                "profit": 2.3
            },
        ]
        executable_tasks = self.service.find_most_profitable_subset_among_some_compatible_subsets(
            input_tasks)
        self.assertEqual(executable_tasks.tasks, expected_result)
