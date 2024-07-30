from rest_framework import serializers

from articles.models import Article


class PublicArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'description',
            'author'
        ]

class PublicArticleDetailSerializer(serializers.ModelSerializer):
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
        ]

class PrivateArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'visibility',
            'title',
            'description',
            'content',
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        # validated_data['author'] == user
        new_article = Article.objects.create(
            author=user,
            **validated_data
        )
        return new_article
    
    def update(self, instance, validated_data):
        
        for field, value in validated_data.items():
            setattr(instance, field, value)

        return instance

