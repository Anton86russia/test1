import django_filters
from .models import Task
from django import forms

class TaskFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Фильтр по дате'
    )

    class Meta:
        model = Task
        fields = ['date', 'is_completed']