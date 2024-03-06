from django.test import Client, TestCase
from ..models import Task
import json


class TasksViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        return super().setUp()

    def test_post_tasks_with_no_queued_tasks_in_db(self):
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
        expected_tasks = [
            {
                "id": 1,
                "name": "upgrade to v2.1",
                "resources": ['proc'],
                "profit": 2.3
            },
            {
                "id": 3,
                "name": "capture for client 1509",
                "resources": [
                        "disk",
                        "cam"
                ],
                "profit": 5.0
            },
            {
                "id": 2,
                "name": "run healthcheck",
                "resources": [],
                "profit": 0.4
            },
        ]
        response = self.client.post('/api/tasks',  json.dumps(input_tasks),
                                    content_type="application/json").json()
        self.assertEqual(response['tasks'], expected_tasks)
        self.assertEqual(response['total_profit'], 7.7)

        db_tasks = Task.objects.filter(status='PROCESSING')
        self.assertEqual(len(db_tasks), 3)

    def test_post_tasks_with_queued_tasks_in_db(self):
        db_tasks = [
            {
                "name": "capture for client 1509",
                "resources": ["disk", "cam"],
                "status": "IN_QUEUE",
                "profit": 5
            },

            {
                "name": "clean disk",
                "resources": ['disk'],
                "status": "IN_QUEUE",
                "profit": 0.4
            },
        ]
        Task.objects.bulk_create(
            [
                Task(name=task["name"], resources=task["resources"],
                     status=task["status"], profit=task["profit"]) for task in db_tasks
            ]
        )
        input_tasks = [
            {
                "name": "upgrade to v2.1",
                "resources": ['proc'],
                "profit": 2.3
            },
            {
                "name": "update cam driver",
                "resources": ['disk', 'cam'],
                "profit": 3.1
            },
        ]
        expected_tasks = [
            {
                "id": 4,
                "name": "capture for client 1509",
                "resources": ["disk", "cam"],
                "profit": 5.0
            },
            {
                "id": 6,
                "name": "upgrade to v2.1",
                "resources": ['proc'],
                "profit": 2.3
            },
        ]

        response = self.client.post('/api/tasks',  json.dumps(input_tasks),
                                    content_type="application/json").json()
        self.assertEqual(response['tasks'], expected_tasks)
        self.assertEqual(response['total_profit'], 7.3)

        processing_tasks = Task.objects.filter(status='PROCESSING')
        self.assertEqual(len(processing_tasks), 2)
        in_queue_tasks = Task.objects.filter(status='IN_QUEUE')
        self.assertEqual(len(in_queue_tasks), 2)

    def test_processing_tasks_are_not_used_while_determining_next_tasks(self):
        db_tasks = [
            {
                "name": "upgrade to v2.1",
                "resources": ['proc'],
                "status": "PROCESSING",
                "profit": 2.3
            },
            {
                "name": "clean disk",
                "resources": ['disk'],
                "status": "PROCESSING",
                "profit": 0.4
            },
        ]
        Task.objects.bulk_create(
            [
                Task(name=task["name"], resources=task["resources"],
                     status=task["status"], profit=task["profit"]) for task in db_tasks
            ]
        )
        input_tasks = [
            {
                "name": "capture for client 1509",
                "resources": ["disk", "cam"],
                "profit": 5
            },
            {
                "name": "update cam driver",
                "resources": ['disk', 'cam'],
                "profit": 3.1
            },
        ]
        expected_result = [
            {
                "id": 10,
                "name": "capture for client 1509",
                "resources": ["disk", "cam"],
                "profit": 5.0
            }
        ]

        response = self.client.post('/api/tasks',  json.dumps(input_tasks),
                                    content_type="application/json").json()
        self.assertEqual(response['tasks'], expected_result)
        self.assertEqual(response['total_profit'], 5)

        processing_tasks = Task.objects.filter(status='PROCESSING')
        self.assertEqual(len(processing_tasks), 3)
        in_queue_tasks = Task.objects.filter(status='IN_QUEUE')
        self.assertEqual(len(in_queue_tasks), 1)
