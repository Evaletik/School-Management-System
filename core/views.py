from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any
from django.views.generic import View, ListView, DetailView, TemplateView, UpdateView, FormView
from django.http import JsonResponse
from django.urls import reverse_lazy

from .models import *
from .forms import *

from schedule.models import *
from grades.models import *

# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"


class GroupLessonsListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = "core/student/my_schedule.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['assignments'] = Assignment.objects.filter(lesson__group__id=self.kwargs["pk"])
        return context


class GroupAttendancesListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = "core/teacher/attendance.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['attendances'] = Attendance.objects.filter(student__group__id=self.kwargs["pk"])
        return context


class GroupListView(ListView):
    model = Group
    template_name = "core/group/group_list.html"
    context_object_name = "groups"

class GroupDetailView(DetailView):
    model = Group
    template_name = "core/group/group_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["students"] = Student.objects.filter(group__id=self.kwargs["pk"])
        return context


class Assignments(ListView):
    model = Assignment
    template_name = "core/teacher/assignments.html"
    context_object_name = 'assignments'

    def get_queryset(self):
        teacher = Teacher.objects.get(id=self.request.user.id)
        assignments = Assignment.objects.filter(lesson__teacher=teacher)

        for assignment in assignments:
            assignment.present_students_count = assignment.attendance_set.filter(status='P').count()

        return assignments


class FindTeacherView(ListView):
    model = Assignment
    template_name = "core/teacher/find_teacher_schedule.html"


def get_teachers(request):
    search = request.GET.get('q')
    teachers = Teacher.objects.filter(firstName__startswith=search)
    payload = []
    for teacher in teachers:
        payload.append({
            "id": teacher.id,
            "full_name": teacher.firstName + ' ' + teacher.lastName,
        })
    return JsonResponse({'payload': payload})


class AssignmentUpdateView(UpdateView):
    model = Assignment
    # form_class = AssignmentForm
    template_name = "core/teacher/assignment_update_form.html"
    context_object_name = 'assignment'
    success_url = reverse_lazy('index')

    # def form_valid(self, form):
    #     print(form)
    #     return super().form_valid(form)
