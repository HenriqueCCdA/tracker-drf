from datetime import datetime

import pytest

from tracker.core.models import Project


@pytest.fixture
def project(db):
    return Project.objects.create(name="Projeto 1")


def test_create(project):
    assert project.pk
    assert Project.objects.exists()


def test_str(project):
    assert str(project) == "Projeto 1"


def test_positive_default(project):
    assert project.is_active


def test_create_at_and_modified_at(project):
    assert isinstance(project.created_at, datetime)
    assert isinstance(project.modified_at, datetime)
