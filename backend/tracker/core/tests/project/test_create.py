from django.shortcuts import resolve_url
from rest_framework import status

from tracker.core.models import Project

URL = "core:lc-project"


def test_positive(client_api, project_data):
    url = resolve_url(URL)

    resp = client_api.post(url, data=project_data, format="json")

    assert resp.status_code == status.HTTP_201_CREATED

    project_db = Project.objects.first()

    body = resp.json()

    assert body["id"] == project_db.pk
    assert body["name"] == project_db.name
    assert body["is_active"]
    assert body["created_at"] == str(project_db.created_at.astimezone().isoformat())
    assert body["modified_at"] == str(project_db.modified_at.astimezone().isoformat())

    assert resp["Location"] == f"http://testserver/project/{project_db.id}/"


def test_negative_missing_field(client_api):
    url = resolve_url(URL)

    resp = client_api.post(url, data={}, format="json")

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body["name"] == ["Este campo é obrigatório."]
