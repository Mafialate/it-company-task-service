from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date

from task.models import (
    Position,
    TaskType,
    Team,
    Project,
    Task
)


class ModelTests(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Python Developer")
        self.task_type = TaskType.objects.create(name="UI Design")

        self.worker = get_user_model().objects.create_user(
            username="andrii_best",
            password="password123",
            position=self.position
        )

        # Создаем команду и добавляем воркера
        self.team = Team.objects.create(name="Dev Avengers")
        self.team.workers.add(self.worker)

        self.project = Project.objects.create(
            name="Task Manager Project",
            deadline=date(2026, 12, 31)
        )
        self.project.teams.add(self.team)

        self.task = Task.objects.create(
            name="Implement Modals",
            deadline=date(2026, 12, 31),
            project=self.project,
            task_type=self.task_type,
            priority=Task.Priority.HIGH
        )

    # 1. Test Position
    def test_position_str(self):
        self.assertEqual(str(self.position), "Python Developer")

    # 2. Test TaskType
    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "UI Design")

    # 3. Test Worker
    def test_worker_str(self):
        self.assertEqual(str(self.worker), "andrii_best - Python Developer")

    def test_worker_projects_property(self):
        self.assertIn(self.project, self.worker.projects)
        self.assertEqual(self.worker.projects.count(), 1)

    # 4. Test Team
    def test_team_str(self):
        self.assertEqual(str(self.team), "Dev Avengers")

    def test_team_tasks_property(self):
        self.assertIn(self.task, self.team.tasks)
        self.assertEqual(self.team.tasks.count(), 1)

    # 5. Test Project
    def test_project_str(self):
        self.assertEqual(str(self.project), "Task Manager Project")

    def test_project_workers_method(self):
        workers = self.project.workers()
        self.assertIn(self.worker, workers)
        self.assertEqual(workers.count(), 1)

    # 6. Test Task
    def test_task_str(self):
        self.assertEqual(str(self.task), "Implement Modals - High")

    def test_task_default_priority(self):
        new_task = Task.objects.create(
            name="Simple Task",
            deadline=date(2026, 12, 31),
            project=self.project,
            task_type=self.task_type
        )
        self.assertEqual(new_task.priority, Task.Priority.MEDIUM)
