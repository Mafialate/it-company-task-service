from django.contrib.auth.models import AbstractUser
from django.db import models

from it_company_task_service import settings


class Position(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name="workers",
        null=True,
    )

    @property
    def projects(self):
        return Project.objects.filter(teams__workers=self).distinct()

    def __str__(self):
        position = self.position.name if self.position else "No position"
        return f"{self.username} - {position}"


class Team(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    workers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="teams",
    )

    @property
    def tasks(self):
        return Task.objects.filter(project__teams=self).distinct()

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    description = models.TextField(blank=True)
    deadline = models.DateField()
    teams = models.ManyToManyField(Team, related_name="projects")

    def workers(self):
        return Worker.objects.filter(
            teams__projects=self
        ).select_related("position").distinct()

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "Urgent", "Urgent"
        HIGH = "High", "High"
        MEDIUM = "Medium", "Medium"
        LOW = "Low", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    workers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.PROTECT,
        related_name="tasks",
    )

    def __str__(self):
        return f"{self.name} - {self.priority}"
