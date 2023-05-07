from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Creation Date and Time"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modificatioin Date and Time"), auto_now=True)

    is_active = models.BooleanField("Ativo", default=True)

    class Meta:
        abstract = True


class Project(BaseModel):
    name = models.CharField(_("Name"), max_length=100)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Task(BaseModel):
    description = models.CharField(_("Descriação"), max_length=1000)
    duration = models.PositiveIntegerField(_("Duração em sengundo"))

    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)

    class Meta:
        ordering = ("description",)

    def __str__(self):
        return self.description
