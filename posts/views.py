from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like
from .serializers.serializers import PostSerializer, CommentSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, которое позволяет только владельцам объекта редактировать его.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешения на чтение разрешены для любого запроса
        if request.method in permissions.SAFE_METHODS:
            return True

        # Права на запись есть только у владельца объекта
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с постами
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        # Проверяем, есть ли уже лайк от этого пользователя
        like_exists = Like.objects.filter(user=user, post=post).exists()
        
        if like_exists:
            # Если лайк уже существует, удаляем его (снимаем лайк)
            Like.objects.filter(user=user, post=post).delete()
            return Response({'status': 'like removed'})
        else:
            # Если лайка нет, создаем его
            Like.objects.create(user=user, post=post)
            return Response({'status': 'like added'})
