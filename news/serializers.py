"""Serializers for the news application API."""

from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """Serialize approved news articles for API responses."""

    author = serializers.StringRelatedField()
    publisher = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "summary",
            "content",
            "author",
            "publisher",
            "approved",
            "approved_at",
            "created_at",
            "updated_at",
        ]
