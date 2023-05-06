import pytest
from faker import Faker
from model_bakery import baker
from rest_framework.test import APIClient

from tracker.core.models import Project

fake = Faker()


@pytest.fixture
def client_api():
    return APIClient()


@pytest.fixture
def project(db):
    return baker.make(Project)


@pytest.fixture
def project_list(db):
    baker.make(Project, _quantity=2, is_active=False)
    baker.make(Project, _quantity=3, is_active=True)

    return Project.objects.all()


@pytest.fixture
def project_data(db):
    return {"name": fake.sentence(nb_words=5)}
