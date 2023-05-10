from django.shortcuts import resolve_url
from model_bakery import baker
from rest_framework import status

from tracker.core.models import Task

URL = "core:lc-task"


def test_positive(client_api, task_list):
    url = resolve_url(URL)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    db_list = Task.objects.filter(is_active=True).order_by("description")

    assert body["count"] == 3

    for r, db in zip(body["results"], db_list):
        assert r["id"] == db.pk
        assert r["description"] == db.description
        assert r["duration"] == db.duration
        assert r["project"] == f"http://testserver/project/{db.project.pk}/"
        assert r["is_active"]
        assert r["created_at"] == str(db.created_at.astimezone().isoformat())
        assert r["modified_at"] == str(db.modified_at.astimezone().isoformat())


def test_positive_filter_by_description(client_api, project):
    baker.make(Task, description="Casa", project=project)
    baker.make(Task, description="CasaCom", project=project)
    baker.make(Task, description="Com", project=project)

    url = resolve_url(URL)

    resp = client_api.get(url + "?q=Casa")

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    assert body["count"] == 2


def test_negative_filter_by_description(client_api, project):
    baker.make(Task, description="Casa", project=project)
    baker.make(Task, description="CasaCom", project=project)
    baker.make(Task, description="Com", project=project)

    url = resolve_url(URL)

    resp = client_api.get(url + "?q=No")

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    assert body["count"] == 0
