from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.users import (FollowsListSerializer, FollowsSerializer,
                                   UserSerializer)
from users.models import Follow, User


class UsersViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'delete', 'head']


class FollowsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        data = {'user': request.user.id, 'following': id}
        serializer = FollowsSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        follow = get_object_or_404(
            Follow, user=user, following=following
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowsListAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = FollowsListSerializer(
            page, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
