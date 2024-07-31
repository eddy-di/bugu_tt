from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied

from accounts.models import User
from articles.models import Article
from articles.serializers import (
    PublicArticleListSerializer,
    PublicArticleDetailSerializer,
    PrivateArticleListSerializer,
    PrivateArticleDetailSerializer
)


class PublicListView(ListAPIView):
    queryset = Article.objects.filter(visibility=Article.PUBLIC).all()
    serializer_class = PublicArticleListSerializer
    permission_classes = [permissions.AllowAny]


class PublicDetailView(RetrieveAPIView):
    queryset = Article.objects.filter(visibility=Article.PUBLIC)
    serializer_class = PublicArticleDetailSerializer
    permission_classes = [permissions.AllowAny]


class PrivateListCreateView(ListCreateAPIView):
    queryset = Article.objects.filter(visibility=Article.PRIVATE).all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PrivateArticleDetailSerializer
        return PrivateArticleListSerializer
    
    def post(self, request, *args, **kwargs):
        if request.user.role != User.AUTHOR:
            raise PermissionDenied(
                {'detail': 'You are not allowed to perform this action.'},
                code=status.HTTP_403_FORBIDDEN
            )
        result = super().post(request, *args, **kwargs)
        request.data['author'] = request.user
        return result
    

class PrivateDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PrivateArticleDetailSerializer

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


