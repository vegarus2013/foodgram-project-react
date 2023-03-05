from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.recipes import IngredientsViewSet, RecipesViewSet, TagsViewSet
from api.views.users import UsersViewSet

app_name = 'api'

router = DefaultRouter()
router.register('ingredients', IngredientsViewSet)
router.register('tags', TagsViewSet)
router.register('recipes', RecipesViewSet)
router.register('users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
