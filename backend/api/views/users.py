from django.db import IntegrityError
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers.users import FollowsSerializer, UserSerializer
from users.models import Follow, User


class UsersViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    @action(
        detail=True, methods=('post', 'delete'),
        permission_classes=(IsAuthenticated, ),
        serializer_class=FollowsSerializer,
    )
    def subscribe(self, request, **kwargs):
        following = self.get_object()
        user = self.request.user

        if user == following:
            return Response(
                {'message': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'POST':
            try:
                subscribtion = Follow.objects.create(
                    user=user,
                    following=following
                )
            except IntegrityError:
                return Response(
                    {'message': 'Вы уже подписаны на этого автора'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = self.get_serializer(
                subscribtion,
                context={'request': request},
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(Follow, user=user, following=following).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, permission_classes=(IsAuthenticated, ))
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowsSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
