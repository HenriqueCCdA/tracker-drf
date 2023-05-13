import pytest
from faker import Faker
from model_bakery import baker
from rest_framework.test import APIClient

from tracker.core.models import Project, Task

fake = Faker()


@pytest.fixture
def client_api():
    return APIClient()


@pytest.fixture
def project(db):
    return baker.make(Project)


@pytest.fixture
def task(db, project):
    return baker.make(Task, project=project)


@pytest.fixture
def project_list(db):
    baker.make(Project, _quantity=2, is_active=False)
    baker.make(Project, _quantity=3, is_active=True)

    return Project.objects.all()


@pytest.fixture
def task_list(project):
    baker.make(Task, _quantity=2, is_active=False, project=project)
    baker.make(Task, _quantity=3, is_active=True, project=project)

    return Task.objects.all()


@pytest.fixture
def project_data(db):
    return {"name": fake.sentence(nb_words=5)}


@pytest.fixture
def task_data(project):
    return {
        "description": fake.sentence(nb_words=5),
        "duration": 1000,
        "project": project.pk,
    }


@pytest.fixture
def update_task(task):
    return {
        "description": "New description",
        "duration": 200,
        "project": task.project.pk,
    }
