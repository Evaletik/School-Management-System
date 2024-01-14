from django.contrib import admin
from .models import *


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ("student", "assignment", "status")
    list_display = ("student", "assignment", "status")
    list_per_page = 10


@admin.register(Mark)
class TeacherAdmin(admin.ModelAdmin):
    pass