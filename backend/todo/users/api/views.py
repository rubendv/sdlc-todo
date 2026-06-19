from django.contrib.auth import logout
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from todo.users.models import User

from .serializers import UserSerializer


class UserViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    def perform_destroy(self, instance) -> None:
        # Check before deletion (delete() clears the pk).
        deleting_self = instance == self.request.user
        super().perform_destroy(instance)
        if deleting_self:
            # Flush the session so no stale session remains; the auth token is
            # removed by the FK cascade. Only on self-delete: deleting another
            # user (e.g. a future admin path) must not log the actor out.
            logout(self.request)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
