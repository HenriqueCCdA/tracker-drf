from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("project/<int:pk>/", views.rud_project, name="rdu-project"),
    path("project/", views.lc_project, name="lc-project"),
    #
    path("task/", views.lc_task, name="lc-task"),
    path("task/<int:pk>/", views.ru_task, name="ru-task"),
]
