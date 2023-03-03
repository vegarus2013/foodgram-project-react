from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.serializers.recipes import RecipeRepresentationSerializer
from recipes.models import Recipe


def add_object_model(model, user, pk):
    if model.objects.filter(user=user, recipe__id=pk).exists():
        return Response({
            'errors': 'Рецепт уже добавлен в список'
        }, status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(Recipe, id=pk)
    model.objects.create(user=user, recipe=recipe)
    serializer = RecipeRepresentationSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_object_model(model, user, pk):
    obj = model.objects.filter(user=user, recipe__id=pk)
    if obj.exists():
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({
        'errors': 'Рецепт уже удален'
    }, status=status.HTTP_400_BAD_REQUEST)
