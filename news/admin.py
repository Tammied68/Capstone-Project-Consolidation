"""Admin registrations for the news application."""

from django.contrib import admin

from .models import APIClientSubscription, Article, Publisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "website")
    search_fields = ("name", "website")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publisher", "approved", "approved_by")
    list_filter = ("approved",)
    search_fields = ("title", "summary", "content")


@admin.register(APIClientSubscription)
class APIClientSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("client_name", "api_key")
    search_fields = ("client_name", "api_key")
    filter_horizontal = ("subscribed_journalists", "subscribed_publishers")