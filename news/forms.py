"""
Forms for the News application.

This module defines Django forms used to create and manage
news-related content, including articles submitted by journalists.
Forms may enforce role-based behavior and input constraints.
"""

from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    """
    Form for creating and submitting news articles.

    Used by journalists to draft articles for editorial review.
    The form dynamically adjusts field requirements based on
    the authenticated user's role.
    """

    class Meta:
        model = Article
        fields = ["title", "summary", "content", "publisher"]

    def __init__(self, *args, **kwargs):
        """
        Initialize the article form with optional user context.

        If a journalist is logged in, the publisher field is made
        optional to allow independent article submissions.

        Args:
            *args: Positional arguments passed to the parent form.
            **kwargs: Keyword arguments, optionally including
                a `user` instance representing the logged-in user.
        """
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user and user.role == "journalist":
            self.fields["publisher"].required = False
