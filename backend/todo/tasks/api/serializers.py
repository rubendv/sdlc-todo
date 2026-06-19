from __future__ import annotations

from rest_framework import serializers

from todo.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer[Task]):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "completed",
            "owner",
            "created_at",
            "updated_at",
        ]
        # Mass-assignment guard (SR-8): owner is server-set, never client-supplied.
        read_only_fields = ["id", "owner", "created_at", "updated_at"]
