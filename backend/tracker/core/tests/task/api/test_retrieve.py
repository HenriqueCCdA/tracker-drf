from django.shortcuts import resolve_url
from rest_framework import status

URL = "core:ru-task"


def test_positive(client_api, task):
    url = resolve_url(URL, pk=task.pk)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    assert body["id"] == task.pk
    assert body["description"] == task.description
    assert body["duration"] == task.duration
    assert body["project_id"] == task.project.pk
    assert body["project_name"] == task.project.name
    assert body["project_url"] == f"http://testserver/project/{task.project.pk}/"
    assert body["is_active"]
    assert body["created_at"] == str(task.created_at.astimezone().isoformat())
    assert body["modified_at"] == str(task.modified_at.astimezone().isoformat())


def test_negative_project_inative_should_return_404(client_api, task):
    url = resolve_url(URL, pk=task.pk)

    task.is_active = False
    task.save()

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body == {"detail": "Não encontrado."}


def test_negative_project_invalid_id(client_api, project):
    url = resolve_url(URL, pk=404)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body == {"detail": "Não encontrado."}
