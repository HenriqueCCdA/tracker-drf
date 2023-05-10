from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from tracker.core.models import Project, Task
from tracker.core.serializers import ProjectSerializer, TaskSerializer


class RetrieveUpdateDestroyProject(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        """
        Lendo um `Projeto` por `id`. Apenas possivel ler projetos `ativos`.
        """
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Atualização completa de um `Projeto`. Apenas possivel aatualizar projetos `ativos`"""
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Atualização parcial de um `Projeto`. Apenas possivel aatualizar projetos `ativos`"""
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Deletando um `Projeto`. O projeto `não` é deletado do banco de dados apenas é marcado como inativo
        """
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ListCreateProject(ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter(is_active=True)

    def post(self, request, *args, **kwargs):
        """Criando um `Projeto´."""
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Lista todos os `Projetos` ativos."""
        return super().get(request, *args, **kwargs)


class ListCreateTask(ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(is_active=True)

    def get_queryset(self):
        queryset = super().get_queryset()
        if q := self.request.query_params.get("q"):
            queryset = queryset.filter(description__icontains=q)
        return queryset


class RetrieveUpdateTask(RetrieveUpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(is_active=True)


rud_project = RetrieveUpdateDestroyProject.as_view()
lc_project = ListCreateProject.as_view()

lc_task = ListCreateTask.as_view()
ru_task = RetrieveUpdateTask.as_view()
