from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import FeedbackForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from .models import Blog
from .forms import CommentForm
from .models import Comment  # Импорт модели комментариев
from .forms import BlogForm
from django.views.decorators.http import require_POST
from .models import Branch
from django.contrib.auth.decorators import login_required
from .models import CarouselImage
from .models import CompanyVideo# Импорт новой модели
from django.shortcuts import get_object_or_404, redirect

from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from django.views.generic import UpdateView, DeleteView
#from django_filters.views import FilterView
#from .filters import TaskFilter
from django.urls import reverse_lazy  # Добавьте эту строку в начале файла
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная страница',  # Переведено
            'year':datetime.now().year,
        }
    )


def about(request):
    carousel_images = CarouselImage.objects.all().order_by('-created_at')[:5]
    latest_video = CompanyVideo.objects.last()  # Последнее загруженное видео

    return render(request, 'app/about.html', {
        'title': 'О нас',
        'message': 'Описание вашего приложения.',
        'carousel_images': carousel_images,
        'latest_video': latest_video,
    })

def blog_list(request):
    posts = Blog.objects.all().order_by('-posted')
    return render(request, 'app/blog/blog_list.html', {'posts': posts})

def links(request):
    return render(request, 'app/links.html', {'title': 'Полезные ресурсы'})

def feedback(request):
    context = dict()  # Создаем переменную-словарь
    
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Сохраняем данные в словарь
            context["data"] = {
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"] or "Не указан",
                "rating": form.cleaned_data["rating"],
                "favorite_section": dict(form.fields["favorite_section"].choices)[form.cleaned_data["favorite_section"]],
                "newsletter": "Да" if form.cleaned_data["newsletter"] else "Нет",
                "message": form.cleaned_data["message"] or "Нет сообщения",
                "visit_date": form.cleaned_data["visit_date"].strftime("%d.%m.%Y")
            }
            return render(request, "app/pool.html", context)
        else:
            context["form"] = form
            return render(request, "app/pool.html", context)
    else:
        context["form"] = FeedbackForm()
        return render(request, "app/pool.html", context)

#регистрация

def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('login')
        else:
            # Передаем форму с ошибками в шаблон
            messages.error(request, 'Исправьте ошибки в форме')
            return render(request, 'app/registration.html', {'regform': form})
    else:
        form = UserCreationForm()
    return render(request, 'app/registration.html', {'regform': form})

#блог

def blog_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_detail.html', {'post': post})

def blog(request):
    posts = Blog.objects.all()
    return render(request, 'app/blog.html', {'title': 'Блог', 'posts': posts, 'year': datetime.now().year})

def blogpost(request, parametr):
    post = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=post)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('blogpost', parametr=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'app/blogpost.html', {
        'post_1': post,
        'comments': comments,
        'form': form,
        'year': datetime.now().year
    })

def newpost(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog')
    else:
        form = BlogForm()
    
    return render(request, 'app/newpost.html', {
        'form': form,
        'title': 'Новая статья',
        'year': datetime.now().year
    })

def videopost(request):
    return render(request, 'app/videopost.html', {
        'title': 'Видео',
        'year': datetime.now().year
    })

# app/views.py
def contact(request):
    branches = Branch.objects.all()  # Берем данные из БД
    current_day = datetime.now().strftime('%A')  # Для подсветки дня
    
    return render(request, 'app/contact.html', {
        'title': 'Контакты',
        'branches': branches,
        'current_day': current_day
    })

def contacts_view(request):
    return render(request, 'app/contact.html', {
        'title': 'Контакты',
    })



class DiaryBaseView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'now': timezone.now(),
            'today_url': reverse_lazy('today_tasks'),
            'tomorrow_url': reverse_lazy('tomorrow_tasks'),
            'past_url': reverse_lazy('past_tasks'),
            'new_task_url': reverse_lazy('new_task')
        })
        return context



class TodayTasksView(DiaryBaseView, ListView):
    model = Task
    template_name = 'app/diary.html'

    def get_queryset(self):
        return Task.objects.filter(
            date=timezone.now().date()
        ).select_related('user')  # Добавлено

class TomorrowTasksView(DiaryBaseView, ListView):
    model = Task
    template_name = 'app/diary.html'

    def get_queryset(self):
        return Task.objects.filter(
            date=timezone.now().date() + timezone.timedelta(days=1)
        )

class PastTasksView(DiaryBaseView, ListView):
    model = Task
    template_name = 'app/diary.html'

    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user,
            date__lt=timezone.now().date()
        ).order_by('-date')

class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'app/task_form.html'
    success_url = reverse_lazy('today_tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timezone'] = timezone  # Добавляем timezone в контекст
        return context

    def test_func(self):
        # Разрешаем доступ только staff-пользователям
        return self.request.user.is_staff

    def get_form_kwargs(self):
        # Убираем поле user из аргументов формы
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'user': self.request.user}
        return kwargs

    def form_valid(self, form):
        # Автоматически устанавливаем пользователя перед сохранением
        form.instance.user = self.request.user
        return super().form_valid(form)



@csrf_protect
@require_POST
def toggle_task(request, pk):
    # Определяем AJAX-запрос
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if not request.user.is_authenticated:
        if is_ajax:
            return JsonResponse({'error': 'Login required'}, status=403)
        messages.warning(request, "Требуется авторизация.")
        return redirect('today_tasks')

    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        if is_ajax:
            return JsonResponse({'error': 'Task not found'}, status=404)
        messages.warning(request, "Задача не найдена.")
        return redirect('today_tasks')

    if task.user != request.user:
        if is_ajax:
            return JsonResponse(
                {'error': 'Нельзя редактировать чужую задачу.'},
                status=403
            )
        messages.warning(request, "Нельзя редактировать чужую задачу.")
        return redirect('today_tasks')

    task.is_completed = not task.is_completed
    task.save()

    if is_ajax:
        return JsonResponse({
            'pk': task.pk,
            'is_completed': task.is_completed,
        })

    messages.success(request, "Статус задачи обновлён.")
    return redirect(request.META.get('HTTP_REFERER', '/'))
    



class FutureTasksView(DiaryBaseView, ListView):
    model = Task
    template_name = 'app/diary.html'

    def get_queryset(self):
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        return Task.objects.filter(
            user=self.request.user,
            date__gt=tomorrow  # Дата позже завтра
        ).order_by('date')


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'app/task_edit.html'
    success_url = reverse_lazy('today_tasks')

    def dispatch(self, request, *args, **kwargs):
        try:
            task = self.get_object()
        except Task.DoesNotExist:
            messages.warning(request, "Задача не найдена.")
            return redirect(self.success_url)

        if not request.user.is_superuser and task.user != request.user:
            messages.warning(request, "Вы не можете редактировать чужую задачу.")
            return redirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.get_object()
        return context


from django.contrib import messages
from django.shortcuts import redirect

class TaskDeleteView(DiaryBaseView, DeleteView):
    model = Task
    template_name = 'app/confirm_delete.html'
    success_url = '/diary/today/'

    def dispatch(self, request, *args, **kwargs):
        try:
            task = self.get_object()
        except self.model.DoesNotExist:
            messages.warning(request, "Задача не найдена.")
            return redirect(self.success_url)

        if not request.user.is_superuser and task.user != request.user:
            messages.warning(request, "Вы не можете удалить чужую задачу.")
            return redirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class DiaryBaseView(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'future_url': reverse_lazy('future_tasks'),  # Добавьте это
        })
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'app/task_detail.html'
    context_object_name = 'task'



@login_required
@require_POST
def toggle_warning(request, branch_id):
    if request.user.is_superuser:
        branch = get_object_or_404(Branch, id=branch_id)
        branch.is_warning = not branch.is_warning
        branch.save()
    return redirect('contact')


