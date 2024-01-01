from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("groups", GroupListView.as_view(), name='group_list'),
    path("groups/<int:pk>/", GroupDetailView.as_view(), name='group_detail'),
    path("groups/<int:pk>/lessons", GroupLessonsListView.as_view(), name='group_lessons'),
    path("groups/<int:pk>/attendances", AttendancesListView.as_view(), name='group_attendances'),
    path("my_schedule", MySchedule.as_view(), name='my_schedule')
    # path("teacher/<int:pk>/schedule", MySchedule.as_view(), name='my_schedule')
    # path("group/<int:pk>/schedule", MySchedule.as_view(), name='my_schedule')
]
