# Third Party Stuff
from base import response
from django.core.exceptions import ImproperlyConfigured


class MultipleSerializerMixin(object):
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:
        class MyViewSet(MultipleSerializerMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }
            @list_route
            def my_action:
                ...
        If there's no serializer available for that action than
        the default serializer class will be returned as fallback.
        """
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class PartialUpdateMixin:
    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return response.Ok(self.get_serializer(instance).data)

    def perform_update(self, serializer):
        serializer.save()
