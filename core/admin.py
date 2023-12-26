from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *
from .resources import AssignmentResource


# Register your models here.
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 10


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)
    list_per_page = 10


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    search_fields = ("group", "teacher", "subject")
    list_display = ("group", "teacher", "subject")
    list_per_page = 10


@admin.register(Assignment)
class AssignmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ("lesson", "due_date", "description", "title")
    list_display = ("lesson", "due_date", "description", "title")
    list_per_page = 10
    resource_class = AssignmentResource


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ("student", "assignment", "status")
    list_display = ("student", "assignment", "status")
    list_per_page = 10


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Mark)
class TeacherAdmin(admin.ModelAdmin):
    pass
