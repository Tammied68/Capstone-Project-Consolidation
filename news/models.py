"""
Database models for the News application.

Defines publishers, articles, newsletters, and API client subscriptions,
including validation and permission-related constraints.
"""

from django.conf import settings
from django.db import models


class Publisher(models.Model):
    """Represents a news publisher."""

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Article(models.Model):
    """Represents a news article authored by a journalist and reviewed by an editor."""

    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    content = models.TextField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles_authored",
        limit_choices_to={"role": "journalist"},
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        help_text="Leave blank for independently published articles.",
    )

    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(blank=True, null=True)

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles_approved",
        limit_choices_to={"role": "editor"},
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [("can_approve_article", "Can approve article")]

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """Represents a newsletter written by a journalist."""

    title = models.CharField(max_length=200)
    content = models.TextField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="newsletters_authored",
        limit_choices_to={"role": "journalist"},
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="newsletters",
        help_text="Leave blank for independently published newsletters.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class APIClientSubscription(models.Model):
    """Stores API client subscriptions for publisher/journalist article access."""

    client_name = models.CharField(max_length=150, unique=True)
    api_key = models.CharField(max_length=255, unique=True)

    subscribed_journalists = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="api_followers",
        limit_choices_to={"role": "journalist"},
    )

    subscribed_publishers = models.ManyToManyField(
        Publisher,
        blank=True,
        related_name="api_subscribers",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["client_name"]

    def __str__(self):
        return self.client_name
