from datetime import datetime

from tracker.core.models import Task


def test_create(task):
    assert task.pk
    assert Task.objects.exists()


def test_str(task):
    assert str(task) == task.description


def test_fields(task):
    assert task._meta.get_field("description")
    assert task._meta.get_field("duration")
    assert task._meta.get_field("project")


def test_default(task):
    assert task.is_active


def test_create_at_and_modified_at(task):
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.modified_at, datetime)


def test_relations(task, project):
    assert task.project == project

    assert project.tasks.count() == 1
