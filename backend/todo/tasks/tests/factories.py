from __future__ import annotations

from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from todo.tasks.models import Task
from todo.users.tests.factories import UserFactory


class TaskFactory(DjangoModelFactory[Task]):
    owner = SubFactory(UserFactory)
    title = Faker("sentence", nb_words=4)
    description = Faker("paragraph")
    completed = False

    class Meta:
        model = Task
