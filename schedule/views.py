from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from core.models import Student
from schedule.models import Assignment
from grades.models import *
from django.views.generic import ListView
from core.models import *


class MySchedule(ListView):
    model = Assignment
    template_name = "core/student/my_schedule.html"

    def get_context_data(self, **kwargs):
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
    

class SubjectScheduleListView(ListView):
    model = Subject
    template_name = "schedules/subject_schedule.html"
    context_object_name = 'assignments'

    def get_queryset(self):
        return Assignment.objects.filter(lesson__subject_id=self.kwargs['pk'])


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