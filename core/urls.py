from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("groups", GroupListView.as_view(), name='group_list'),


    path("groups/<int:pk>/", GroupDetailView.as_view(), name='group_detail'),
    path("groups/<int:pk>/lessons", GroupLessonsListView.as_view(), name='group_lessons'),
    path("groups/<int:pk>/attendances", GroupAttendancesListView.as_view(), name='group_attendances'),
    path("assignments", Assignments.as_view(), name='assignments'),
    path("assignments/<int:pk>/set_attendances", SetAttendance.as_view(), name='set_attendances'),

    path("my_schedule", MySchedule.as_view(), name='my_schedule'),
    path("teacher/<int:pk>/schedule", TeacherScheduleListView.as_view(), name='teacher_schedule'),
    path("group/<int:pk>/schedule", GroupScheduleListView.as_view(), name='group_schedule'),

    path("find_teacher", FindTeacherView.as_view(), name='find_teacher'),
    path("find_teacher/search", get_teachers, name='find_teacher_a'),

    path("assignments/<int:pk>/edit", AssignmentUpdateView.as_view(), name='edit_assignment'),
]
