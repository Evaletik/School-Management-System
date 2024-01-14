from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from core.models import Student
from schedule.models import Assignment
from grades.models import *
from django.views.generic import ListView
from core.models import *
from django.http import JsonResponse


class MySchedule(ListView):
    model = Assignment
    template_name = "core/student/my_schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group: Group = Student.objects.get(id=self.request.user.id).group
        context['assignments'] = Assignment.objects.filter(lesson__group__id=user_group.id)
        return context


class TeacherScheduleListView(View):
    template_name = "schedules/teacher_schedule.html"


    def get_teachers_payload(self, name):
        teachers = Teacher.objects.filter(Q(firstName__contains=name) | Q(lastName__contains=name))
        payload = [{
            "id": teacher.id,
            "full_name": teacher.firstName + ' ' + teacher.lastName,
        } for teacher in teachers]
        return JsonResponse({'payload': payload})
    
    
    def get(self, request, *args, **kwargs):
        name = request.GET.get('name')
        teacher_id = request.GET.get('teacher_id')
        if name:
            return self.get_teachers_payload(name)
        elif teacher_id:
            teacher = Teacher.objects.filter(id=teacher_id).first()
            context = {
                'teacher': teacher,
                'assignments': Assignment.objects.filter(lesson__teacher=teacher)
            }
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name)


class GroupScheduleListView(ListView):
    model = Assignment
    template_name = "core/group/schedule.html"
    context_object_name = 'assignments'

    def get_queryset(self):
        group = Group.objects.values('id').get(id=self.kwargs['pk'])
        return Assignment.objects.filter(lesson__group=group['id'])
    

class SubjectScheduleListView(View):
    template_name = "schedules/subject_schedule.html"

    def get_subjects_payload(self, name):
        subjects = Subject.objects.filter(name__contains=name)
        payload = [{
            "id": subject.id,
            "name": subject.name,
        } for subject in subjects]
        return JsonResponse({'payload': payload})
    
    def get_assignments_context(self, subject, teacher_id=None):
        teachers = Teacher.objects.filter(subjects=subject)
        if teacher_id:
            teacher = teachers.filter(id=teacher_id).first()
        else:
            teacher = teachers.first()

        assignments = Assignment.objects.filter(lesson__teacher=teacher, lesson__subject=subject)
        return {
            'subject': subject,
            'teachers': teachers,
            'assignments': assignments
        }

    def get(self, request, *args, **kwargs):
        name = request.GET.get('name')
        subject_id = request.GET.get('subject_id')
        teacher_id = request.GET.get('teacher_id')

        if name:
            return self.get_subjects_payload(name)
        elif subject_id:
            subject = Subject.objects.filter(id=subject_id).first()
            context = self.get_assignments_context(subject, teacher_id)
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name)

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