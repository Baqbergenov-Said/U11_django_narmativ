from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('tasks/', views.task_list, name='tasks'),
    path('tasks/create/', views.create_task, name='task_create'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:pk>/update/', views.update_task, name='update_task'),
    path('<path:path>', views.page_not_found, name='catch_all'),
]