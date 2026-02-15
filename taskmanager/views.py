from django.shortcuts import render, redirect, get_object_or_404

from .models import Task

def homepage(request):
    return render(request, 'homepage.html')

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        doe_date = request.POST.get('doe_date')
        status = request.POST.get('status', 'pending')
        Task.objects.create(title=title, description=description, doe_date=doe_date, status=status)
        return redirect('task_list')
    return render(request, 'create_task.html')

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_delete.html', {'task': task})

def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.status = request.POST.get('status', task.status)
        task.save()
        return redirect('task_list')
    return render(request, 'edit_task.html', {'task': task})

def page_not_found(request, path=None, exception=None):
    return render(request, 'not_found.html', status=404)