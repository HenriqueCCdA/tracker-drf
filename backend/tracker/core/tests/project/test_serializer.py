import pytest
from django.test import RequestFactory

from tracker.core.models import Project
from tracker.core.serializers import ProjectSerializer


def test_positive_serialization_one_obj(project):
    request = RequestFactory().request()

    serializer = ProjectSerializer(instance=project, context={"request": request})

    data = serializer.data

    assert data["id"] == project.pk
    assert data["name"] == project.name
    assert data["is_active"] == project.is_active
    assert data["created_at"] == str(project.created_at.astimezone().isoformat())
    assert data["modified_at"] == str(project.modified_at.astimezone().isoformat())
    assert data["url"] == f"http://testserver/project/{project.pk}/"


def test_positive_serialization_objs_list(project_list):
    request = RequestFactory().request()

    serializer = ProjectSerializer(instance=Project.objects.all(), many=True, context={"request": request})

    for data, db in zip(serializer.data, project_list):
        assert data["id"] == db.pk
        assert data["name"] == db.name
        assert data["is_active"] == db.is_active
        assert data["created_at"] == str(db.created_at.astimezone().isoformat())
        assert data["modified_at"] == str(db.modified_at.astimezone().isoformat())
        assert data["url"] == f"http://testserver/project/{db.pk}/"


def test_positive_create(project_data):
    serializer = ProjectSerializer(data=project_data)

    assert serializer.is_valid()

    project = serializer.save()

    assert project.pk
    assert Project.objects.exists()


@pytest.mark.parametrize(
    "field",
    [
        "name",
    ],
)
def test_negative_missing_fields(field, project_data):
    data = project_data.copy()

    del data[field]

    serializer = ProjectSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors[field] == ["Este campo é obrigatório."]
