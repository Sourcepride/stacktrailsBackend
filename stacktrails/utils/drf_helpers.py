from django.shortcuts import get_object_or_404
from rest_framework import viewsets, response, serializers


class CustomModelViewSet(viewsets.ModelViewSet):
    def get_object(self):
        queryset = self.get_queryset()

        if isinstance(self.lookup_field, (list, tuple)):
            filters = {field: self.kwargs[field] for field in self.lookup_field}
        else:
            filters = {self.lookup_field: self.kwargs[self.lookup_field]}

        obj = get_object_or_404(queryset, **filters)
        self.check_object_permissions(self.request, obj)
        return obj

    def invalidate_prefetch_cache(self, instance):
        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}


def default_detail_as_view_mapping():
    return {
        "get": "retrieve",
        "patch": "partial_update",
        "put": "update",
        "delete": "destroy",
    }


def default_as_view_mapping():
    return {"get": "list", "post": "create"}


class SerializedRepresentationRelatedField(serializers.RelatedField):
    def __init__(self, **kwargs):
        self.serializer_class = kwargs.pop("serializer_class")
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        data = int(data) if str(data).isdigit() else data

        if not isinstance(data, int):
            raise serializers.ValidationError(
                {f"{self.field_name}": f"{self.field_name} id must be an integer"}
            )

        queryset = self.queryset.filter(id=data)
        if not queryset.exists():
            raise serializers.ValidationError(
                {f"{self.field_name}": f"no {self.field_name} with id {data} exists"}
            )

        return queryset.first()

    def to_representation(self, value):
        return self.serializer_class(value, context=self.context).data
