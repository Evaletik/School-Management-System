from django.db import models


# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=20)


class Group(models.Model):
    name = models.CharField(max_length=20)
    # students
    # lessons


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    # teacher
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)


class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    due_date = models.DateTimeField()
    description = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    mark = models.DecimalField(max_digits=3, decimal_places=2)


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("A", "Absent"),
        ("P", "Present"),
        ("E", "Excused")
    ]
    # student
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)
