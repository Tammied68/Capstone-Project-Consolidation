"""
Database models for the News application.

This module defines core content models including publishers,
articles, newsletters, and API client subscriptions. Models enforce
role-based constraints and support both authenticated web access
and API consumption.
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Publisher(models.Model):
    """
    Represents a publishing organization.

    Publishers may be associated with journalists, articles,
    newsletters, and subscribers. Articles may also be published
    independently without an associated publisher.
    """

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """
        Return the publisher's display name.
        """
        return self.name


class Article(models.Model):
    """
    Represents a news article written by a journalist.

    Articles require editorial approval before becoming publicly
    visible. Each article may optionally be associated with a
    publisher and includes metadata about its approval status.
    """

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

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles_approved",
        limit_choices_to={"role": "editor"},
    )
