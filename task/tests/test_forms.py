from datetime import date, timedelta
from django.test import TestCase
from task.forms import (
    PositionSearchForm,
    WorkerCreateForm,
    ProjectCreateForm,
    validate_deadline
)
from task.models import Team

class FormTests(TestCase):

    def test_position_search_form_placeholder(self):
        form = PositionSearchForm()
        self.assertIn('placeholder="Search your position"', form.as_p())
        self.assertFalse(form.fields["name"].required)

    def test_worker_create_form_fields(self):
        form = WorkerCreateForm()
        expected_fields = ["username", "first_name", "last_name", "position"]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_validate_deadline_past_date(self):
        past_date = date.today() - timedelta(days=1)
        with self.assertRaises(Exception) as context:
            validate_deadline(past_date)
        self.assertIn("Incorrect deadline", str(context.exception))

    def test_validate_deadline_today_or_future(self):
        today = date.today()
        future_date = date.today() + timedelta(days=5)
        self.assertEqual(validate_deadline(today), today)
        self.assertEqual(validate_deadline(future_date), future_date)

    def test_project_create_form_invalid_deadline(self):
        team = Team.objects.create(name="QA Team")
        form_data = {
            "name": "Invalid Project",
            "deadline": date.today() - timedelta(days=1),
            "teams": [team.id],
            "description": "Short description"
        }
        form = ProjectCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)
        self.assertEqual(form.errors["deadline"], ["Incorrect deadline"])

    def test_project_create_form_valid_data(self):
        team = Team.objects.create(name="Dev Team")
        form_data = {
            "name": "Cool Project",
            "deadline": date.today() + timedelta(days=1),
            "teams": [team.id],
            "description": "Valid data project"
        }
        form = ProjectCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
