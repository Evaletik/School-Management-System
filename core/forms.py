from django.contrib.admin.widgets import AdminSplitDateTime
from django import forms
from .models import *


class AssignmentForm(forms.ModelForm):
    from_date = forms.SplitDateTimeField(widget=AdminSplitDateTime())
    to_date = forms.SplitDateTimeField(widget=AdminSplitDateTime())

    class Meta:
        model = Assignment
        fields = ['from_date', 'to_date']
