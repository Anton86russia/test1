"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import date
from .models import Comment
from .models import Blog
from django import forms
from .models import Task
from django.utils import timezone
from django.contrib.auth.models import User  # Импорт модели пользователя
from app.models import Task, Tag

def validate_visit_date(value):
    min_date = date(1920, 1, 1)  # Минимум 1 января 1920 года
    max_date = date.today()       # Максимум — текущая дата
    
    if value < min_date:
        raise ValidationError("Дата не может быть раньше 01.01.1920!")
    if value > max_date:
        raise ValidationError("Дата не может быть в будущем!")

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class FeedbackForm(forms.Form):
    # Обязательное текстовое поле
    name = forms.CharField(
        label="Ваше имя",
        min_length=2,
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={"required": "Это поле обязательно!"}
    )
    
    # обязательное email-поле
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    
    # Радиокнопки для оценки (1-5)
    RATING_CHOICES = [(i, f"Оценка {i}") for i in range(1, 6)]
    rating = forms.ChoiceField(
        label="Оцените сайт",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        initial=5
    )
    
    # Выпадающий список
    SITE_SECTIONS = [
        ("design", "Дизайн"),
        ("content", "Контент"),
        ("navigation", "Навигация")
    ]
    favorite_section = forms.ChoiceField(
        label="Любимый раздел",
        choices=SITE_SECTIONS,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    # Флажок
    newsletter = forms.BooleanField(
        label="Подписаться на новости",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    
    # Многострочное текстовое поле
    message = forms.CharField(
        label="Ваши предложения",
        widget=forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        required=False
    )
    
    # Поле с валидацией даты
    visit_date = forms.DateField(
        label="Дата посещения",
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control",
            "min": "1920-01-01",          # Ограничение в HTML
            "max": date.today().strftime("%Y-%m-%d")  # Динамическое значение
        }),
        validators=[validate_visit_date],  # Серверная валидация
        error_messages={
            "required": "Укажите дату посещения!"
        }
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'summary', 'image', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label="Теги",
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'date', 'user', 'tags']
        labels = {
            'title': 'Название задачи',
            'description': 'Описание',
            'date': 'Дата выполнения',
            'user': 'Автор задачи',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise ValidationError("Дата не может быть в прошлом!")
        return date

class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label="Теги",
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'date', 'user', 'tags', 'image']  # Добавлено image
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'})  # Добавить виджет
        }