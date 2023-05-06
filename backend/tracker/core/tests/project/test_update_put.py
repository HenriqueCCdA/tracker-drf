from django.shortcuts import resolve_url
from rest_framework import status

URL = "core:rdu-project"


def test_positive(client_api, project):
    url = resolve_url(URL, pk=project.pk)

    resp = client_api.put(url, data={"name": "New Project Name"}, format="json")

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    project.refresh_from_db()

    assert body["id"] == project.pk
    assert body["name"] == project.name
    assert body["is_active"]
    assert body["created_at"] == str(project.created_at.astimezone().isoformat())
    assert body["modified_at"] == str(project.modified_at.astimezone().isoformat())


def test_negative_invalid_id(client_api, project):
    url = resolve_url(URL, pk=404)

    resp = client_api.put(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_project_inative_should_return_404(client_api, project):
    url = resolve_url(URL, pk=project.pk)

    project.is_active = False
    project.save()

    resp = client_api.put(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body == {"detail": "Não encontrado."}


def test_negative_missing_field(client_api, project):
    pk = project.pk

    url = resolve_url(URL, pk=pk)

    resp = client_api.put(url, data={}, format="json")

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body["name"] == ["Este campo é obrigatório."]
