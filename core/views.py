from typing import Any
from django.views.generic import ListView, DetailView, TemplateView
from .models import *


# Create your views here.
class HomeView(TemplateView):
    template_name = "index.html"


class GroupLessonsListView(ListView):
    model = Lesson
    template_name = "core/group_lessons_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['assignments'] = Assignment.objects.filter(lesson__group__id=self.kwargs["pk"])
        return context


class GroupListView(ListView):
    model = Group
    template_name = "core/group_list.html"


class GroupDetailView(DetailView):
    model = Group
    template_name = "core/group_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["students"] = Student.objects.filter(group__id=self.kwargs["pk"])
        return context
