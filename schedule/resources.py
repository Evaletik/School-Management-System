from import_export import resources
from .models import Assignment


class AssignmentResource(resources.ModelResource):

    class Meta:
        model = Assignment
