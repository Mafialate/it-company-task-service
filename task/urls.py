from django.urls import path

from task.views import (
    index,
    TaskTypeListView,
    TaskTypeDeleteView,
    TaskTypeUpdateView,
    TaskTypeCreateView,
    TaskListView,
    TaskUpdateView,
    TaskDeleteView,
    TaskCreateView,
    TaskDetailView,
    WorkerListView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView,
    WorkerDetailView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    TeamListView,
    TeamCreateView,
    ProjectListView,
    ProjectCreateView,
    TeamDetailView,
    TeamUpdateView,
    TeamDeleteView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    contact_us,
    privacy
)

urlpatterns = [
    path("", index, name='index'),
# TaskType
    path("task-type/", TaskTypeListView.as_view(), name='task-type-list'),
    path(
        "task-type/create/",
        TaskTypeCreateView.as_view(),
        name='task-type-create'
    ),
    path(
        "task-type/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name='task-type-update'
    ),
    path(
        "task-type/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name='task-type-delete'
    ),
# Task
    path("task/", TaskListView.as_view(), name='task-list'),
    path("task/<int:pk>/", TaskDetailView.as_view(), name='task-detail'),
    path("task/create/", TaskCreateView.as_view(), name='task-create'),
    path(
        "task/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name='task-update'
    ),
    path(
        "task/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name='task-delete'
    ),
# Worker
    path("worker/", WorkerListView.as_view(), name='worker-list'),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name='worker-detail'),
    path("worker/create/", WorkerCreateView.as_view(), name='worker-create'),
    path(
        "worker/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name='worker-update'
    ),
    path(
        "worker/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name='worker-delete'
    ),
# Position
    path("position/", PositionListView.as_view(), name='position-list'),
    path(
        "position/create/",
        PositionCreateView.as_view(),
        name='position-create'
    ),
    path(
        "position/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name='position-update'
    ),
    path(
        "position/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name='position-delete'
    ),
# Team
    path("team/", TeamListView.as_view(), name='team-list'),
    path("team/<int:pk>/", TeamDetailView.as_view(), name='team-detail'),
    path("team/create/", TeamCreateView.as_view(), name='team-create'),
    path(
        "team/<int:pk>/update/",
        TeamUpdateView.as_view(),
        name='team-update'
    ),
    path(
        "team/<int:pk>/delete/",
        TeamDeleteView.as_view(),
        name='team-delete'
    ),
# Project
    path("project/", ProjectListView.as_view(), name='project-list'),
    path(
        "project/<int:pk>/",
        ProjectDetailView.as_view(),
        name='project-detail'
    ),
    path(
        "project/create/",
        ProjectCreateView.as_view(),
        name='project-create'
    ),
    path(
        "project/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name='project-update'
    ),
    path(
        "project/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name='project-delete'
    ),
# Contact us
    path("contact-us/", contact_us, name='contact-us'),
# Privacy
    path("privacy/", privacy, name='privacy'),
]

app_name = "task"
