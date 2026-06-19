from __future__ import annotations

from rest_framework.viewsets import ModelViewSet

from todo.tasks.models import Task

from .serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    # Required by DjangoModelPermissions to resolve the model; scoped in get_queryset.
    queryset = Task.objects.all()

    def get_queryset(self):
        # Object-level scoping (SR-6 / SR-9): own rows only, no admin bypass.
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer) -> None:
        # owner is server-set from the authenticated user (SR-7).
        serializer.save(owner=self.request.user)
