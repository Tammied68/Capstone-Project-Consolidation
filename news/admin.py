from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Article, Newsletter, Publisher, APIClientSubscription


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "created_at")
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "publisher",
        "approved",
        "approved_by",
        "created_at",
    )
    list_filter = ("approved", "publisher", "created_at")
    search_fields = ("title", "content")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publisher", "created_at")
    list_filter = ("publisher", "created_at")
    search_fields = ("title", "content")


@admin.register(APIClientSubscription)
class APIClientSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("client_name", "api_key", "created_at")
    search_fields = ("client_name",)