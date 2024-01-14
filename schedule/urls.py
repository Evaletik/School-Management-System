from django.urls import path
from .views import *
from .models import *
    

urlpatterns = [
    path("my", MySchedule.as_view(), name='my_schedule'),
    path("teacher", TeacherScheduleListView.as_view(), name='teacher_schedule'),
    path("group/<int:pk>", GroupScheduleListView.as_view(), name='group_schedule'),
    path("subject", SubjectScheduleListView.as_view(), name='subject_schedule'),

    # ?????
    path("assignments/<int:pk>/set-attendances/", SetAttendance.as_view(), name='set_attendances'),
]