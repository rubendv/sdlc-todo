from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from todo.tasks.api.views import TaskViewSet
from todo.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("tasks", TaskViewSet)


app_name = "api"
urlpatterns = router.urls
