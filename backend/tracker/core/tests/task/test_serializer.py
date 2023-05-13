import pytest
from django.test import RequestFactory

from tracker.core.models import Task
from tracker.core.serializers import TaskSerializer


def test_positive_serialization_one_obj(task):
    request = RequestFactory().request()

    serializer = TaskSerializer(instance=task, context={"request": request})

    data = serializer.data

    assert data["id"] == task.pk
    assert data["description"] == task.description
    assert data["duration"] == task.duration
    assert data["project_id"] == task.project.pk
    assert data["project_name"] == task.project.name
    assert data["project_url"] == f"http://testserver/project/{task.project.pk}/"
    assert data["is_active"] == task.is_active
    assert data["created_at"] == str(task.created_at.astimezone().isoformat())
    assert data["modified_at"] == str(task.modified_at.astimezone().isoformat())
    assert data["url"] == f"http://testserver/task/{task.pk}/"


def test_positive_serialization_objs_list(task_list):
    request = RequestFactory().request()

    serializer = TaskSerializer(instance=Task.objects.all(), many=True, context={"request": request})

    for data, db in zip(serializer.data, task_list):
        assert data["id"] == db.pk
        assert data["description"] == db.description
        assert data["duration"] == db.duration
        assert data["project_id"] == db.project.pk
        assert data["project_name"] == db.project.name
        assert data["project_url"] == f"http://testserver/project/{db.project.pk}/"
        assert data["is_active"] == db.is_active
        assert data["created_at"] == str(db.created_at.astimezone().isoformat())
        assert data["modified_at"] == str(db.modified_at.astimezone().isoformat())
        assert data["url"] == f"http://testserver/task/{db.pk}/"


def test_positive_create(task_data):
    serializer = TaskSerializer(data=task_data)

    assert serializer.is_valid()

    task = serializer.save()

    assert task.pk
    assert Task.objects.exists()


@pytest.mark.parametrize(
    "field",
    [
        "description",
        "duration",
        "project",
    ],
)
def test_negative_missing_fields(field, task_data):
    data = task_data.copy()

    del data[field]

    serializer = TaskSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors[field] == ["Este campo é obrigatório."]


@pytest.mark.parametrize(
    "field,value,error",
    [
        ("duration", -1, "Certifque-se de que este valor seja maior ou igual a 0."),
        ("duration", "aa", "Um número inteiro válido é exigido."),
        ("project", 2, 'Pk inválido "2" - objeto não existe.'),
        ("project", "/project/1/", "Tipo incorreto. Esperado valor pk, recebeu str."),
    ],
)
def test_negative_invalid_fields(field, value, error, task_data):
    data = task_data.copy()

    data[field] = value

    serializer = TaskSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors[field] == [error]
