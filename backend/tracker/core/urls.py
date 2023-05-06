from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("project/<int:pk>/", views.rud_project, name="rdu-project"),
    path("project/", views.lc_project, name="lc-project"),
]
