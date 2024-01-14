from import_export.admin import ImportExportModelAdmin
from .resources import AssignmentResource
from django.contrib import admin
from .models import *


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    search_fields = ("group", "teacher", "subject")
    list_display = ("group", "teacher", "subject")
    list_per_page = 10


@admin.register(Assignment)
class AssignmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ("lesson", "from_date", "to_date", "description", "title")
    list_display = ("lesson", "from_date", "to_date", "description", "title")
    list_per_page = 10
    resource_class = AssignmentResource