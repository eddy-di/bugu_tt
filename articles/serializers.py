from rest_framework import serializers

from accounts.models import User
from articles.models import Article


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
        ]


class PublicArticleListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'description',
            'author'
        ]

class PublicArticleDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'description',
            'content',
            'author'
        ]

class PrivateArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'visibility',
            'title',
            'description',
            'author'
        ]
    
    def create(self, validated_data):
        new_article = Article.objects.create(
            **validated_data,
            author=self.context["request"].user,
        )
        return new_article

class PrivateArticleDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Article
        fields = [
            'id',
            'visibility',
            'title',
            'description',
            'content',
            'author'
        ]

    def create(self, validated_data):
        if 'author' not in validated_data:
            new_article = Article.objects.create(
                **validated_data,
                author=self.context["request"].user,
            )
        return new_article
    
    def update(self, instance, validated_data):
        
        for field, value in validated_data.items():
            setattr(instance, field, value)

        return instance

