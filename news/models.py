from django.db import models

# Create your models here.
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Article(models.Model):
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
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ("can_approve_article", "Can approve article"),
        ]

    def clean(self):
        super().clean()

        if self.author and self.author.role != "journalist":
            raise ValidationError("Only journalists can be authors of articles.")

        if self.approved_by and self.approved_by.role != "editor":
            raise ValidationError("Only editors can approve articles.")

    def __str__(self):
        return self.title


class Newsletter(models.Model):
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

    def clean(self):
        super().clean()

        if self.author and self.author.role != "journalist":
            raise ValidationError("Only journalists can create newsletters.")

    def __str__(self):
        return self.title


class APIClientSubscription(models.Model):
    client_name = models.CharField(max_length=150, unique=True)
    api_key = models.CharField(max_length=255, unique=True)
    subscribed_publishers = models.ManyToManyField(
        Publisher,
        blank=True,
        related_name="api_subscribers",
    )
    subscribed_journalists = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="api_followers",
        limit_choices_to={"role": "journalist"},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["client_name"]

    def __str__(self):
        return self.client_name