from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied

from accounts.models import User
from articles.models import Article
from articles.serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer
)


class ArticleListCreateView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArticleDetailSerializer
        return ArticleListSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Article.objects.all()
        else:
            return Article.objects.filter(visibility=Article.PUBLIC)

    def post(self, request, *args, **kwargs):
        if request.user.role != User.AUTHOR:
            raise PermissionDenied(
                {'detail': 'You are not allowed to perform this action.'},
                code=status.HTTP_403_FORBIDDEN
            )
        result = super().post(request, *args, **kwargs)
        request.data['author'] = request.user
        return result
    

class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ArticleDetailSerializer

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_authenticated:
            if obj.visibility == Article.PUBLIC:
                return obj
            raise PermissionDenied(
                {'detail': 'You are not allowed to access this article.'},
                code=status.HTTP_403_FORBIDDEN
            )
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role != User.AUTHOR:
            raise PermissionDenied(
                {'detail': 'You are not allowed to perform this action.'},
                code=status.HTTP_403_FORBIDDEN
            )
        if instance.author != request.user:
            raise PermissionDenied(
                {'detail': 'You are not allowed to perform this action.'},
                code=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role != User.AUTHOR:
            raise PermissionDenied(
                {'detail': 'You are not allowed to perform this action.'},
                code=status.HTTP_403_FORBIDDEN
            )
        if instance.author != request.user:
            raise PermissionDenied(
                {'detail': 'You are not allowed to perform this action.'},
                code=status.HTTP_403_FORBIDDEN
            )
        return super().delete(request, *args, **kwargs)


