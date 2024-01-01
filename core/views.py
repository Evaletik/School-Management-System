from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any
from django.views.generic import ListView, DetailView, TemplateView
from .models import *


# Create your views here.
class HomeView(TemplateView):
    template_name = "index.html"


class GroupLessonsListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = "core/student/my_schedule.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['assignments'] = Assignment.objects.filter(lesson__group__id=self.kwargs["pk"])
        return context


class AttendancesListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = "core/teacher/attendance.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['attendances'] = Attendance.objects.filter(student__group__id=self.kwargs["pk"])
        return context


class GroupListView(ListView):
    model = Group
    template_name = "core/group_list.html"


class GroupDetailView(DetailView):
    model = Group
    template_name = "core/group_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["students"] = Student.objects.filter(group__id=self.kwargs["pk"])
        return context


class MySchedule(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = "core/student/my_schedule.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_group: Group = Student.objects.get(id=self.request.user.id).group
        context['assignments'] = Assignment.objects.filter(lesson__group__id=user_group.id)
        return context
