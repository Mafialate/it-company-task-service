from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from task.forms import TaskTypesSearchForm, PositionSearchForm, WorkerSearchForm, WorkerCreateForm, \
    WorkerPositionUpdateForm, ProjectSearchForm, ProjectUpdateForm, TaskSearchForm, PositionUpdateForm, TaskCreateForm, \
    TaskUpdateForm, TeamSearchForm, TeamCreateForm, TeamUpdateForm, ProjectCreateForm
from task.models import Position, TaskType, Task, Team, Project


@login_required
def index(request: HttpRequest) -> HttpResponse:
    tasks_num = Task.objects.count()
    task_types_num = TaskType.objects.count()
    workers_num = get_user_model().objects.count()
    positions_num = Position.objects.count()
    projects_num = Project.objects.count()
    teams_num = Team.objects.count()

    context = {
        "tasks_num": tasks_num,
        "task_types_num": task_types_num,
        "workers_num": workers_num,
        "positions_num": positions_num,
        "projects_num": projects_num,
        "teams_num": teams_num,
    }

    return render(request, "task/index.html", context=context)

#Contact us page
@login_required
def contact_us(request: HttpRequest) -> HttpResponse:
    return render(request, "task/page-contact-us.html")

#Privacy page
@login_required
def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, "task/page-privacy.html")

#TaskType CRUD
class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = "task/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskTypesSearchForm(self.request.GET)

        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        query = self.request.GET.get("name")

        if query:
            return queryset.filter(name__icontains=query)

        return queryset


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "task/task_type_form.html"
    success_url = reverse_lazy("task:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "task/task_type_form.html"
    success_url = reverse_lazy("task:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskType
    template_name = "task/task_type_confirm_delete.html"
    success_url = reverse_lazy("task:task-type-list")

#Task CRUD
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm(self.request.GET)

        return context

    def get_queryset(self):
        queryset = (
            Task.objects.all()
            .select_related("project", "task_type")
            .prefetch_related("workers")
        )
        query = self.request.GET.get("name")

        if query:
            return queryset.filter(name__icontains=query)

        return queryset


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("task:task-list")


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy("task:task-list")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")

#Worker CRUD
class WorkerListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerSearchForm(self.request.GET)

        return context

    def get_queryset(self):
        queryset = get_user_model().objects.all().select_related("position")
        query = self.request.GET.get("username")

        if query:
            return queryset.filter(username__icontains=query)

        return queryset


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    fields = "__all__"

    def get_queryset(self):
        return get_user_model().objects.all().prefetch_related("teams", "tasks").all()


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = get_user_model()
    form_class = WorkerCreateForm
    success_url = reverse_lazy("task:worker-list")


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = WorkerPositionUpdateForm
    success_url = reverse_lazy("task:worker-list")


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("task:worker-list")

#Position CRUD
class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = PositionSearchForm(self.request.GET)

        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        query = self.request.GET.get("name")

        if query:
            return queryset.filter(name__icontains=query)

        return queryset


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task:position-list")


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    model = Position
    form_class = PositionUpdateForm
    success_url = reverse_lazy("task:position-list")


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    model = Position
    success_url = reverse_lazy("task:position-list")

#Team CRUD
class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    form_class = TeamSearchForm
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TeamSearchForm(self.request.GET)

        return context

    def get_queryset(self):
        queryset = Team.objects.all().prefetch_related("workers")
        query = self.request.GET.get("name")

        if query:
            return queryset.filter(name__icontains=query)

        return queryset


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    fields = "__all__"


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy("task:team-list")


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamUpdateForm
    success_url = reverse_lazy("task:team-list")


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    success_url = reverse_lazy("task:team-list")

#Project CRUD
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    queryset = Project.objects.all().prefetch_related("teams")
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = ProjectSearchForm(self.request.GET)

        return context

    def get_queryset(self):
        queryset = Project.objects.all()
        query = self.request.GET.get("name")

        if query:
            return queryset.filter(name__icontains=query)

        return queryset


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    fields = "__all__"


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    success_url = reverse_lazy("task:project-list")


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectUpdateForm
    success_url = reverse_lazy("task:project-list")


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("task:project-list")
