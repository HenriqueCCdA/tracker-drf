from django.contrib import admin

from tracker.core.models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_active",
        "created_at",
        "modified_at",
    )

    list_filter = ("is_active",)

    search_fields = ("name",)

    readonly_fields = (
        "id",
        "created_at",
        "modified_at",
    )


@admin.register(Task)
class TasktAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "description",
        "duration",
        "project",
        "is_active",
        "created_at",
        "modified_at",
    )

    list_filter = ("is_active",)

    search_fields = ("description",)

    readonly_fields = (
        "id",
        "created_at",
        "modified_at",
    )
