from django.shortcuts import resolve_url
from rest_framework import status

from tracker.core.models import Project

URL = "core:lc-project"


def test_positive(client_api, project_list):
    url = resolve_url(URL)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    db_list = Project.objects.filter(is_active=True).order_by("name")

    assert body["count"] == 3

    for r, db in zip(body["results"], db_list):
        assert r["id"] == db.pk
        assert r["name"] == db.name
        assert r["is_active"]
        assert r["created_at"] == str(db.created_at.astimezone().isoformat())
        assert r["modified_at"] == str(db.modified_at.astimezone().isoformat())
