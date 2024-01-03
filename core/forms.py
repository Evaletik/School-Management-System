from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from .models import *


class AssignmentForm(forms.ModelForm):
    from_date = forms.DateTimeField(widget=AdminDateWidget())
    to_date = forms.DateTimeField()

    class Meta:
        model = Assignment
        fields = ['from_date', 'to_date']
