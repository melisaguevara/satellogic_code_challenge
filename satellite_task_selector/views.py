# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TaskSerializer
from .services import TasksService


class TaskAPIView(APIView):
    def __init__(self, **kwargs):
        self.service = TasksService()
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                most_profitable_tasks = self.service.get_next_batch_of_executable_tasks(
                    serializer.validated_data)
                return Response(most_profitable_tasks, status=status.HTTP_200_OK)
            except:
                return Response({'message': 'Something went wrong.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)
