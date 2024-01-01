from django.db import models
from django.core.exceptions import ValidationError


class Subject(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"


class Group(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    subjects = models.ManyToManyField(Subject)
    birthDate = models.DateField()
    birthPlace = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, )
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.teacher.__str__()} {self.subject.name}'

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"


class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    description = models.CharField(max_length=20)
    title = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"

    def clean(self):
        time_difference_minutes = (self.to_date - self.from_date).total_seconds() / 60

        if not (45 <= time_difference_minutes <= 210):
            raise ValidationError({"to_date":"Time difference must be between 45 minutes and 3.5 hours"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Mark(models.Model):
    id = models.AutoField(primary_key=True)
    mark = models.DecimalField(max_digits=3, decimal_places=2)
    student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True)
    assignment = models.ForeignKey('Assignment', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.student.id} - {self.mark}'

    class Meta:
        verbose_name = "Mark"
        verbose_name_plural = "Marks"


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    lastName = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    birthPlace = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, )
    password = models.CharField(max_length=100)
    birthDate = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("A", "Absent"),
        ("P", "Present"),
        ("E", "Excused")
    ]
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)

    def __str__(self):
        return f'{self.student.id} {self.status}'

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
