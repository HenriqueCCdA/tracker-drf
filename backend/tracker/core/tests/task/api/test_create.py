import pytest
from django.shortcuts import resolve_url
from rest_framework import status

from tracker.core.models import Task

URL = resolve_url("core:lc-task")


def test_positive(client_api, task_data):
    resp = client_api.post(URL, data=task_data, format="json")

    assert resp.status_code == status.HTTP_201_CREATED

    task_db = Task.objects.first()

    body = resp.json()

    assert body["id"] == task_db.pk
    assert body["description"] == task_db.description
    assert body["duration"] == task_db.duration
    assert body["project"] == f"http://testserver/project/{task_db.project.pk}/"
    assert body["is_active"]
    assert body["created_at"] == str(task_db.created_at.astimezone().isoformat())
    assert body["modified_at"] == str(task_db.modified_at.astimezone().isoformat())

    assert resp["Location"] == f"http://testserver/task/{task_db.pk}/"


@pytest.mark.parametrize(
    "field",
    [
        "description",
        "duration",
        "project",
    ],
)
def test_negative_missing_field(client_api, field, task_data):
    data = task_data.copy()

    del data[field]

    resp = client_api.post(URL, data=data, format="json")

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body[field] == ["Este campo é obrigatório."]


@pytest.mark.parametrize(
    "field,value,error",
    [
        ("duration", -1, "Certifque-se de que este valor seja maior ou igual a 0."),
        ("duration", "aa", "Um número inteiro válido é exigido."),
        ("project", 1, "Tipo incorreto. Necessário string URL, recebeu int."),
        ("project", "/project/1/", "Hyperlink inválido - Objeto não existe."),
        ("project", "/task/1/", "Hyperlink inválido - Combinação URL incorreta."),
    ],
)
def test_negative_invalid_fields(client_api, field, value, error, task_data):
    data = task_data.copy()

    data[field] = value

    resp = client_api.post(URL, data=data, format="json")

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body[field] == [error]
