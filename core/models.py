from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=20)

class Group(models.Model):
    name = models.CharField(max_length=20)

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    subjects = models.ManyToManyField(Subject)
    birthDate = models.DateField()
    birthPlace = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    password = models.CharField(max_length=100)

class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    due_date = models.DateTimeField()
    description = models.CharField(max_length=20)
    title = models.CharField(max_length=20)

class Mark(models.Model):
    id = models.AutoField(primary_key=True)
    mark = models.DecimalField(max_digits=3, decimal_places=2)
    student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True)
    assignment = models.ForeignKey('Assignment', on_delete=models.SET_NULL, null=True)

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    lastName = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    birthPlace = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    password = models.CharField(max_length=100)
    birthDate = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    STATUS_CHOICES = [
        ("A", "Absent"),
        ("P", "Present"),
        ("E", "Excused")
    ]
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)