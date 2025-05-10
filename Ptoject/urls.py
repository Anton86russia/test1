from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app.views import toggle_warning
from app.views import TodayTasksView, TomorrowTasksView, PastTasksView, TaskCreateView
from app.views import TaskUpdateView, TaskDeleteView
from app.views import toggle_task  # Добавьте эту строку
from django.urls import path
from app.views import TaskCreateView, FutureTasksView, TaskDetailView

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('links/', views.links, name='links'),
    path("feedback/", views.feedback, name="feedback"),
    path("pool/", views.feedback, name="pool"),
    #админка
    #регистрация
    path('registration/', views.registration, name='registration'),
    #блог
    path('blog/', views.blog, name='blog'),
    path('blog/<int:parametr>/', views.blogpost, name='blogpost'),
    path('blog/newpost/', views.newpost, name='newpost'),
    path('video/', views.videopost, name='videopost'),
    path('toggle-warning/<int:branch_id>/', toggle_warning, name='toggle_warning'),

    path('diary/today/', TodayTasksView.as_view(), name='today_tasks'),
    path('diary/tomorrow/', TomorrowTasksView.as_view(), name='tomorrow_tasks'),
    path('diary/past/', PastTasksView.as_view(), name='past_tasks'),
    path('diary/new/', TaskCreateView.as_view(), name='new_task'),
    path('diary/edit/<int:pk>/', TaskUpdateView.as_view(), name='edit_task'),
    path('diary/delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('toggle-task/<int:pk>/', toggle_task, name='toggle_task'),
    path('diary/future/', FutureTasksView.as_view(), name='future_tasks'),
    path('diary/task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
