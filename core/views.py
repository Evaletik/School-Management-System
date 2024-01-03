from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any
from django.views.generic import View, ListView, DetailView, TemplateView, UpdateView, FormView
from django.http import JsonResponse

from .models import *
from .forms import *


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


class GroupAttendancesListView(LoginRequiredMixin, ListView):
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


class SetAttendance(View):
    # model = Attendance
    # fields = ['status']
    template_name = "core/teacher/set_attendances.html"

    def get(self, request, pk):
        assignment = get_object_or_404(Assignment, id=pk)
        students = Student.objects.filter(group=assignment.lesson.group)
        return render(request, self.template_name, {'assignment': assignment, 'students': students})

    def post(self, request, pk):
        assignment = get_object_or_404(Assignment, id=pk)
        students = Student.objects.filter(group=assignment.lesson.group)
        new_attendances = [
            Attendance(student=student, assignment=assignment,
                       status=request.POST.get(f'student_{student.id}_attendance', 'A'))
            for student in students
            if not assignment.attendance_set.filter(student__id=student.id).count() > 1
        ]

        Attendance.objects.bulk_create(new_attendances)

        return redirect(to="group_attendances", pk=assignment.lesson.group.id)


class MySchedule(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = "core/student/my_schedule.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_group: Group = Student.objects.get(id=self.request.user.id).group
        context['assignments'] = Assignment.objects.filter(lesson__group__id=user_group.id)
        return context


class TeacherScheduleListView(ListView):
    model = Assignment
    template_name = "core/teacher/schedule.html"
    context_object_name = 'assignments'

    def get_queryset(self):
        teacher = Teacher.objects.values('id').get(id=self.kwargs['pk'])
        return Assignment.objects.filter(lesson__teacher=teacher['id'])


class GroupScheduleListView(ListView):
    model = Assignment
    template_name = "core/group/schedule.html"
    context_object_name = 'assignments'

    def get_queryset(self):
        group = Group.objects.values('id').get(id=self.kwargs['pk'])
        return Assignment.objects.filter(lesson__group=group['id'])


class FindTeacherView(ListView):
    model = Assignment
    template_name = "core/find_teacher_schedule.html"


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
    form_class = AssignmentForm
    template_name = "core/teacher/assignment_update_form.html"