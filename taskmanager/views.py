from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Task
from .forms import RegisterForm, LoginForm 

def homepage(request):
    return render(request, 'homepage.html')

def page_not_found(request, path):
    return render(request, 'not_found.html', status=404)

@login_required(login_url='login')
def task_list(request):
    query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page', 1)
    
    tasks_list = Task.objects.filter(user=request.user).order_by('-doe_date')

    if query:
        tasks_list = tasks_list.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(tasks_list, 6) 
    page_obj = paginator.get_page(page_number)

    return render(request, 'task_list.html', {
        'tasks': page_obj, 
        'query': query, 
    })

# sing up view or register view
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# login view or login into view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user'] 
            login(request, user)
            return redirect('tasks')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

# CRUD operations:
@login_required(login_url='login')
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        doe_date = request.POST.get('doe_date')
        status = request.POST.get('status', 'pending')
        Task.objects.create(user=request.user, title=title, description=description, doe_date=doe_date, status=status)
        return redirect('tasks')
    return render(request, 'create_task.html')

@login_required(login_url='login')
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete() 
        return redirect('tasks')
    return render(request, 'task_delete.html', {'task': task})

@login_required(login_url='login')
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.status = request.POST.get('status', task.status)
        task.save()
        return redirect('tasks')
    return render(request, 'edit_task.html', {'task': task})
