import pytest
from django.shortcuts import resolve_url
from rest_framework import status

URL = "core:ru-task"


def test_positive(client_api, update_task, task):
    url = resolve_url(URL, pk=task.pk)

    resp = client_api.put(url, data=update_task, format="json")

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    task.refresh_from_db()

    assert body["id"] == task.pk
    assert body["description"] == task.description
    assert body["duration"] == task.duration
    assert body["project"] == f"http://testserver/project/{task.project.pk}/"
    assert body["is_active"]
    assert body["created_at"] == str(task.created_at.astimezone().isoformat())
    assert body["modified_at"] == str(task.modified_at.astimezone().isoformat())


def test_negative_invalid_id(client_api, task):
    url = resolve_url(URL, pk=404)

    resp = client_api.put(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_project_inative_should_return_404(client_api, task):
    url = resolve_url(URL, pk=task.pk)

    task.is_active = False
    task.save()

    resp = client_api.put(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body == {"detail": "Não encontrado."}


@pytest.mark.parametrize(
    "field",
    [
        "description",
        "duration",
        "project",
    ],
)
def test_negative_missing_field(client_api, field, update_task, task):
    url = resolve_url(URL, pk=task.pk)

    data = update_task.copy()

    del data[field]

    resp = client_api.put(url, data=data, format="json")

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
def test_negative_invalid_fields(client_api, field, value, error, update_task, task):
    url = resolve_url(URL, pk=task.pk)

    data = update_task.copy()

    data[field] = value

    resp = client_api.put(url, data=data, format="json")

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body[field] == [error]
