from django.urls import path
from .views import *

urlpatterns = [
    #Index
    path("", IndexView.as_view(), name='index'),

    # Groups
    path("groups/", GroupListView.as_view(), name='group_list'),
    path("groups/<int:pk>/", GroupDetailView.as_view(), name='group_detail'),
    path("groups/<int:pk>/lessons/", GroupLessonsListView.as_view(), name='group_lessons'),
    path("groups/<int:pk>/attendances/", GroupAttendancesListView.as_view(), name='group_attendances'),

    # Assignments
    path("assignments/", Assignments.as_view(), name='assignments'),
    # path("assignments/<int:pk>/set-attendances/", SetAttendance.as_view(), name='set_attendances'),
    path("assignments/<int:pk>/edit/", AssignmentUpdateView.as_view(), name='edit_assignment'),

    # # Find Teacher
    # path("find-teacher/", FindTeacherView.as_view(), name='find_teacher'),
    # path("find-teacher/search/", get_teachers, name='find_teacher_results'),
]