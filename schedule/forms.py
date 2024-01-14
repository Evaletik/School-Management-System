from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from .models import Assignment


class AssignmentForm(forms.ModelForm):
    from_date = forms.SplitDateTimeField(widget=AdminSplitDateTime())
    to_date = forms.SplitDateTimeField(widget=AdminSplitDateTime())

    class Meta:
        model = Assignment
        fields = ['from_date', 'to_date']