from celery.result import AsyncResult
from django.http import Http404
from rest_framework import views, status
import cluster_tasks
from rest_framework.response import Response

from client.serializers import BaseTaskSerializer
from clb_client.celery import app


class CreateJobAPIView(views.APIView):
    def get_task_serializer_class(self, task):
        return BaseTaskSerializer.for_func(task)

    def get_task_serializer(self, task, data):
        return self.get_task_serializer_class(task)(data=data)

    def post(self, *args, **kwargs):
        task = getattr(cluster_tasks, self.kwargs['task'], None)
        if task is None:
            raise Http404
        serializer = self.get_task_serializer(task, self.request.data)
        if serializer.is_valid(raise_exception=True):
            task = app.task(task).delay(**serializer.data)
            return Response({'task_id': task.id},
                            status=status.HTTP_201_CREATED)


class TaskResultAPIView(views.APIView):
    def get(self, *args, **kwargs):
        res = AsyncResult(self.kwargs['id'], app=app)
        if res.state == 'SUCCESS':
            return Response({
                'result': res.get()
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'result': 'unknown'
            }, status=status.HTTP_200_OK)
