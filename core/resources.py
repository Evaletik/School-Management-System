from import_export import resources
from core.models import Assignment
from import_export.fields import Field
from import_export.widgets import DateWidget


class AssignmentResource(resources.ModelResource):

    class Meta:
        model = Assignment
