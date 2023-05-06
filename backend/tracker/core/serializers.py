from rest_framework import serializers

from tracker.core.models import Project


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

        extra_kwargs = {"url": {"view_name": "core:rdu-project"}, "is_active": {"read_only": True}}
