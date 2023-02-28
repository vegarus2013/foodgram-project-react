from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from api.filters import IngredientsFilter, RecipesFilter, TagsFilter
from api.mixins import ItemMixin
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers.recipes import (FavoritesSerializer,
                                     IngredientsSerializer,
                                     RecipesListSerializer,
                                     RecipesWriteSerializer,
                                     ShoppingCartsSerializer, TagsSerializer)
from recipes.models import (Favorite, Ingredient, IngredientQuantity, Recipe,
                            ShoppingCart, Tag)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TagsFilter
    filter_backends = (DjangoFilterBackend,)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = IngredientsFilter
    filter_backends = (DjangoFilterBackend,)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrReadOnly,)
    filterset_class = RecipesFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipesListSerializer
        return RecipesWriteSerializer

    @action(detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return ItemMixin(request, pk, serializer=FavoritesSerializer).add()

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return ItemMixin(request, pk, Favorite).delete()

    @action(detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return ItemMixin(
            request, pk,
            serializer=ShoppingCartsSerializer
        ).add()

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return ItemMixin(request, pk, ShoppingCart).delete()

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = IngredientQuantity.objects.filter(
            recipe__shopping_carts__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_cart = '\n'.join([
            f'{ingredient["ingredient__name"]} - {ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}'
            for ingredient in ingredients
        ])
        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
