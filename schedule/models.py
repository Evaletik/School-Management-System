from django.core.exceptions import ValidationError
from django.db import models
from core.models import *


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
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