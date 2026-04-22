from datetime import date

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from task.models import Project, Position, Team, Task, Worker


class TaskTypesSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search your task type"}
        )
    )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Search your position"}
        )
    )


class PositionUpdateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        label="Name",
    )

    class Meta:
        model = Position
        fields = "__all__"


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Search your worker by username"}
        )
    )


class WorkerCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "position",)


class WorkerPositionUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["position"]


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Search your project by name"}
        )
    )


class ProjectCreateForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Project
        fields = "__all__"

    def clean_deadline(self):
        return validate_deadline(self.cleaned_data["deadline"])


class ProjectUpdateForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Project
        exclude = ("name",)

    def clean_deadline(self):
        return validate_deadline(self.cleaned_data["deadline"])


def validate_deadline(deadline):
    currant_time = date.today()

    if deadline < currant_time:
        raise ValidationError("Incorrect deadline")

    return deadline


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Search your task by name"}
        )
    )


class TaskCreateForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        exclude = ("is_completed",)

    def clean_deadline(self):
        return validate_deadline(self.cleaned_data["deadline"])


class TaskUpdateForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        exclude = ["name", "project", "task_type"]

    def clean_deadline(self):
        return validate_deadline(self.cleaned_data["deadline"])


class TeamSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Search your team by name"}
        )
    )


class TeamUpdateForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Team
        fields = "__all__"


class TeamCreateForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Team
        fields = "__all__"