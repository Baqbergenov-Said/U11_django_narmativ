from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from .models import Task

def homepage(request):
    return render(request, 'homepage.html')

def task_list(request):
    tasks = Task.objects.all()
    search_query = request.GET.get('search', '')
    
    # Filter tasks by search query
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    
    # Pagination
    paginator = Paginator(tasks, 5)  # 5 tasks per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tasks': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'task_list.html', context)

def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        doe_date = request.POST.get('doe_date')
        status = request.POST.get('status', 'pending')
        Task.objects.create(title=title, description=description, doe_date=doe_date, status=status)
        return redirect('tasks')
    return render(request, 'create_task.html')

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    return render(request, 'task_delete.html', {'task': task})

def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.status = request.POST.get('status', task.status)
        task.save()
        return redirect('tasks')
    return render(request, 'edit_task.html', {'task': task})

def page_not_found(request, path=None, exception=None):
    return render(request, 'not_found.html', status=404)


from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Task

def task_list(request):
    query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page', 1)
    
    tasks_list = Task.objects.all().order_by('-doe_date')

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