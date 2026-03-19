from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    publisher = serializers.SerializerMethodField()

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

    def get_publisher(self, obj):
        return obj.publisher.name if obj.publisher else "Independent"
