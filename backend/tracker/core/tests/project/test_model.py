from datetime import datetime

from tracker.core.models import Project


def test_create(project):
    assert project.pk
    assert Project.objects.exists()


def test_str(project):
    assert str(project) == project.name


def test_default(project):
    assert project.is_active


def test_create_at_and_modified_at(project):
    assert isinstance(project.created_at, datetime)
    assert isinstance(project.modified_at, datetime)
