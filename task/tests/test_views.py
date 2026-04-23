from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task.models import Position, TaskType, Project, Task, Team

POSITION_LIST_URL = reverse("task:position-list")
TASK_TYPE_LIST_URL = reverse("task:task-type-list")
WORKER_LIST_URL = reverse("task:worker-list")
PROJECT_LIST_URL = reverse("task:project-list")
TEAM_LIST_URL = reverse("task:team-list")
TASK_LIST_URL = reverse("task:task-list")


class PublicViewTests(TestCase):
    """Тесты для неавторизованного пользователя (редиректы на логин)"""

    def test_position_list_login_required(self):
        response = self.client.get(POSITION_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_task_type_list_login_required(self):
        res = self.client.get(TASK_TYPE_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_worker_list_login_required(self):
        res = self.client.get(WORKER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_project_list_login_required(self):
        response = self.client.get(PROJECT_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_team_list_login_required(self):
        res = self.client.get(TEAM_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_task_list_login_required(self):
        res = self.client.get(TASK_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        Position.objects.create(name="Developer")
        Position.objects.create(name="Manager")
        self.client.force_login(self.user)

    def test_retrieve_positions(self):
        response = self.client.get(POSITION_LIST_URL)
        positions = Position.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions)
        )
        self.assertTemplateUsed(response, "task/position_list.html")

    def test_retrieve_positions_with_parameters(self):
        response = self.client.get(POSITION_LIST_URL, {"name": "Developer"})
        position = Position.objects.filter(name="Developer")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["position_list"]), 1)
        self.assertEqual(
            list(response.context["position_list"]),
            list(position)
        )


class PrivateWorkerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        get_user_model().objects.create_user(
            username="worker1",
            password="password1",
        )
        get_user_model().objects.create_user(
            username="worker2",
            password="password2",
        )
        self.client.force_login(self.user)

    def test_retrieve_workers(self):
        response = self.client.get(WORKER_LIST_URL)
        workers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["worker_list"]), 3)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(workers)
        )
        self.assertTemplateUsed(response, "task/worker_list.html")

    def test_retrieve_workers_with_parameters(self):
        response = self.client.get(WORKER_LIST_URL, {"username": "worker1"})
        worker = get_user_model().objects.filter(username="worker1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["worker_list"]), 1)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(worker)
        )


class PrivateTaskTypeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        TaskType.objects.create(name="Bug")
        TaskType.objects.create(name="Feature")
        self.client.force_login(self.user)

    def test_retrieve_task_types(self):
        response = self.client.get(TASK_TYPE_LIST_URL)
        task_types = TaskType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_type_list"]),
            list(task_types)
        )
        self.assertTemplateUsed(response, "task/task_type_list.html")

    def test_retrieve_task_types_with_parameters(self):
        response = self.client.get(TASK_TYPE_LIST_URL, {"name": "Bug"})
        task_type = TaskType.objects.filter(name="Bug")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["task_type_list"]), 1)
        self.assertEqual(
            list(response.context["task_type_list"]),
            list(task_type)
        )


class PrivateTeamTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password123"
        )
        self.client.force_login(self.user)
        self.team = Team.objects.create(name="Alpha Team")

    def test_retrieve_teams(self):
        response = self.client.get(TEAM_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.team, response.context["team_list"])
        self.assertTemplateUsed(response, "task/team_list.html")

    def test_search_team_by_name(self):
        Team.objects.create(name="Beta Squad")
        response = self.client.get(TEAM_LIST_URL, {"name": "Alpha"})
        self.assertContains(response, "Alpha Team")
        self.assertNotContains(response, "Beta Squad")


class PrivateProjectTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="project_admin", password="password123"
        )
        self.client.force_login(self.user)
        self.project = Project.objects.create(
            name="Apollo 11",
            deadline=date(2026, 12, 31)
        )

    def test_retrieve_projects(self):
        response = self.client.get(PROJECT_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.project, response.context["project_list"])
        self.assertTemplateUsed(response, "task/project_list.html")

    def test_search_project_by_name(self):
        Project.objects.create(name="Manhattan", deadline=date(2026, 1, 1))
        response = self.client.get(PROJECT_LIST_URL, {"name": "Apollo"})
        self.assertContains(response, "Apollo 11")
        self.assertNotContains(response, "Manhattan")


class PrivateTaskTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="task_user", password="password123"
        )
        self.client.force_login(self.user)

        self.project = Project.objects.create(
            name="Main", deadline=date(2026, 1, 1)
        )
        self.task_type = TaskType.objects.create(name="Bug")

        self.task = Task.objects.create(
            name="Fix critical bug",
            deadline=date(2026, 1, 1),
            project=self.project,
            task_type=self.task_type,
            priority="Urgent"
        )

    def test_retrieve_tasks(self):
        response = self.client.get(TASK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.task, response.context["task_list"])
        self.assertTemplateUsed(response, "task/task_list.html")

    def test_search_task_by_name(self):
        Task.objects.create(
            name="Refactor code",
            deadline=date(2026, 1, 1),
            project=self.project,
            task_type=self.task_type
        )
        response = self.client.get(TASK_LIST_URL, {"name": "Fix"})
        self.assertContains(response, "Fix critical bug")
        self.assertNotContains(response, "Refactor code")
