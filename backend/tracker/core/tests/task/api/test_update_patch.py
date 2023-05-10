import pytest
from django.shortcuts import resolve_url
from model_bakery import baker
from rest_framework import status

from tracker.core.models import Project

URL = "core:ru-task"


@pytest.mark.parametrize(
    "field",
    [
        "description",
        "duration",
    ],
)
def test_positive(client_api, update_task, task, field):
    url = resolve_url(URL, pk=task.pk)

    data = {field: update_task[field]}

    resp = client_api.patch(url, data=data, format="json")

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    task.refresh_from_db()
    assert body[field] == getattr(task, field)


def test_positive_update_project(client_api, task):
    url = resolve_url(URL, pk=task.pk)

    new_project = baker.make(Project)
    data = {"project": resolve_url("core:rdu-project", pk=new_project.pk)}

    resp = client_api.patch(url, data=data, format="json")

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    task.refresh_from_db()
    assert body["project"] == f"http://testserver/project/{new_project.pk}/"


def test_negative_invalid_id(client_api, task):
    url = resolve_url(URL, pk=404)

    resp = client_api.patch(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_project_inative_should_return_404(client_api, task):
    url = resolve_url(URL, pk=task.pk)

    task.is_active = False
    task.save()

    resp = client_api.patch(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body == {"detail": "Não encontrado."}


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
def test_negative_invalid_fields(client_api, field, value, error, task):
    url = resolve_url(URL, pk=task.pk)

    data = {field: value}

    resp = client_api.put(url, data=data, format="json")

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body[field] == [error]
