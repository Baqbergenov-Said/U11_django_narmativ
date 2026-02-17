from django.db import models

#Soft delete model for task, instead of deleting the record from database, we will mark it as deleted by setting is_deleted to True
class TaskQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_deleted=True)

class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db).filter(is_deleted=False)

# Staus choices for task
class Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'

# Task model to store task information
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    doe_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)

    is_deleted = models.BooleanField(default=False)
    
    objects = TaskManager() # Connecting the custom manager to the model, so that we can use it to filter out the deleted records

    def delete(self, *args, **kwargs): # Delete one method to mark the record as deleted instead of actually deleting it from database
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.title
    
# If you dont create this meta class, django will create a table with name taskmanager_task 
    class Meta:
        db_table = 'taskmanager'

