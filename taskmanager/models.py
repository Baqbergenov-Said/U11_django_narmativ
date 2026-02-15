from django.db import models

class Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    doe_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'taskmanager'

