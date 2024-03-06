from datetime import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Task(models.Model):
    STATUS_CHOICES = (
        ('IN_QUEUE', 'In Queue'),
        ('PROCESSING', 'Processing'),
        ('PROCESSED', 'Processed')
    )

    name = models.CharField(max_length=150)
    resources = ArrayField(models.CharField(max_length=50))
    profit = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='IN_QUEUE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_tasks(cls, tasks):
        task_models = [cls(name=task['name'], resources=task['resources'],
                           profit=task['profit']) for task in tasks]
        cls.objects.bulk_create(task_models)

    @classmethod
    def get_tasks_by_status(cls, status):
        return cls.objects.filter(status=status).values('id', 'name', 'resources', 'profit')

    @classmethod
    def update_tasks_status(cls, tasks_ids_to_update, new_status):
        cls.objects.filter(
            id__in=tasks_ids_to_update).update(status=new_status, updated_at=datetime.now())
