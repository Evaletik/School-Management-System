from typing import Any
from django.views.generic import ListView
from .models import *


# Create your views here.
class GroupLessonsListView(ListView):
    model = Lesson
    template_name = "core/group_lessons_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
