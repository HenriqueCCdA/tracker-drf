from django.shortcuts import resolve_url
from rest_framework import status

URL = "core:rdu-project"


def test_positive(client_api, project):
    url = resolve_url(URL, pk=project.pk)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_204_NO_CONTENT

    project.refresh_from_db()

    assert not project.is_active


def test_negative_invalid_id(client_api, project):
    url = resolve_url(URL, pk=404)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_project_inative_should_return_404(client_api, project):
    url = resolve_url(URL, pk=project.pk)

    project.is_active = False
    project.save()

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body == {"detail": "Não encontrado."}
