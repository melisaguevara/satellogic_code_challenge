from rest_framework import serializers
from .models import Task
from .services import TasksSubset


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    resources = serializers.ListField(
        child=serializers.CharField(), allow_empty=True)

    class Meta:
        model = Task
        fields = ['name', 'resources', 'profit']
