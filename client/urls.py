from django.urls import path

from .views import CreateJobAPIView, TaskResultAPIView

urlpatterns = [
    path('create/<str:task>/', CreateJobAPIView.as_view()),
    path('result/<str:id>/', TaskResultAPIView.as_view()),
]