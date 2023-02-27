from django.contrib import admin

from .models import (Favorites, IngredientQuantitys, Ingredients, Recipes,
                     ShoppingCarts, Tags)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'quantity_favorites')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)

    def quantity_favorites(self, obj):
        return obj.favorites.count()


@admin.register(IngredientQuantitys)
class IngredientQuantitysAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(ShoppingCarts)
class ShoppingCartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
