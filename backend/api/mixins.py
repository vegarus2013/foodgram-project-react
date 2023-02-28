from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status

from recipes.models import Recipe


class AbstractGETViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    pass


class ItemMixin:
    def __init__(self, request, pk, model=None, serializer=None) -> None:
        self.request = request
        self.pk = pk
        self.model = model
        self.serializer = serializer

    def add(self):
        data = {'user': self.request.user.id, 'recipe': self.pk}
        serializer = self.serializer(
            data=data, context={'request': self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.pk)
        cart_object = get_object_or_404(
            self.model, user=user, recipe=recipe
        )
        cart_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
