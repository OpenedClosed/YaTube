from rest_framework import mixins, viewsets


class CreateDeleteViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin,
                          mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass
