from rest_framework_nested import routers

from .api import RequestViewSet, ServicesViewSet

default_router = routers.SimpleRouter()

default_router.register("main", RequestViewSet, basename="main")
default_router.register("services", ServicesViewSet, basename="services")

urlpatterns = default_router.urls
