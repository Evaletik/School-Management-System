from django.db import models
from core.models import Student
from schedule.models import Assignment


class Mark(models.Model):
    mark = models.DecimalField(max_digits=3, decimal_places=2)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.student.id} - {self.mark}'

    class Meta:
        verbose_name = "Mark"
        verbose_name_plural = "Marks"


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
