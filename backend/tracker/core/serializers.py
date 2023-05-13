from rest_framework import serializers

from tracker.core.models import PROJECT_NAME_LENGTH, Project, Task


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "is_active",
            "url",
            "created_at",
            "modified_at",
        )

        extra_kwargs = {
            "url": {"view_name": "core:rdu-project"},
            "is_active": {"read_only": True},
        }


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.filter(is_active=True),
        write_only=True,
    )
    project_id = serializers.IntegerField(read_only=True)
    project_name = serializers.CharField(
        max_length=PROJECT_NAME_LENGTH,
        source="project",
        read_only=True,
    )
    project_url = serializers.HyperlinkedRelatedField(
        view_name="core:rdu-project",
        read_only=True,
        source="project",
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "description",
            "duration",
            "project",
            "project_id",
            "project_name",
            "project_url",
            "is_active",
            "url",
            "created_at",
            "modified_at",
        )

        extra_kwargs = {
            "url": {"view_name": "core:ru-task"},
            "is_active": {"read_only": True},
            # "project": {"view_name": "core:rdu-project"},
        }
