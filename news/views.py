"""
Views for the News application.

Handles dashboard rendering, article creation and approval,
email notifications, and API access to subscribed articles.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ArticleForm
from .models import APIClientSubscription, Article
from .serializers import ArticleSerializer


@login_required
def home(request):
    """
    Redirect authenticated users to their role-specific dashboard.

    Readers are redirected to the reader dashboard, journalists to
    the journalist dashboard, and editors to the editor dashboard.
    If no role match is found, a fallback home template is rendered.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponseRedirect or HttpResponse: Redirect to dashboard
        or rendered home page.
    """
    user = request.user

    if user.role == "reader":
        return redirect("reader_dashboard")
    if user.role == "journalist":
        return redirect("journalist_dashboard")
    if user.role == "editor":
        return redirect("editor_dashboard")

    return render(request, "home.html")


@login_required
def reader_dashboard(request):
    """
    Display all approved articles to readers.

    Retrieves articles that have been approved by an editor and
    orders them by publication date.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered reader dashboard page.
    """
    approved_articles = Article.objects.filter(
        approved=True
    ).order_by("-created_at")

    return render(
        request,
        "news/reader_dashboard.html",
        {"approved_articles": approved_articles},
    )


@login_required
def journalist_dashboard(request):
    """
    Display articles authored by the logged-in journalist.

    Journalists can see and manage the articles they have
    created, ordered by most recent first.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered journalist dashboard page.
    """
    my_articles = Article.objects.filter(
        author=request.user
    ).order_by("-created_at")

    return render(
        request,
        "news/journalist_dashboard.html",
        {"my_articles": my_articles},
    )


@login_required
def editor_dashboard(request):
    """
    Display all unapproved articles for editorial review.

    Editors can view articles awaiting approval and
    decide whether to approve or reject them.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered editor dashboard page.
    """
    pending_articles = Article.objects.filter(
        approved=False
    ).order_by("-created_at")

    return render(
        request,
        "news/editor_dashboard.html",
        {"pending_articles": pending_articles},
    )


@login_required
def create_article(request):
    """
    Allow journalists to create and submit articles for editorial approval.

    Validates user role, processes the article submission form,
    assigns the author and publisher where applicable, and
    submits the article for review.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse or HttpResponseRedirect: Rendered form or
        redirect to journalist dashboard.
    """
    if request.user.role != "journalist":
        messages.error(
            request,
            "Only journalists can create articles.",
        )
        return redirect("home")

    if request.method == "POST":
        form = ArticleForm(request.POST, user=request.user)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.approved = False

            if not article.publisher and request.user.publisher:
                article.publisher = request.user.publisher

            article.save()
            messages.success(
                request,
                "Article created successfully and submitted for approval.",
            )
            return redirect("journalist_dashboard")
    else:
        form = ArticleForm(user=request.user)

    return render(
        request,
        "news/create_article.html",
        {"form": form},
    )


@login_required
def pending_articles(request):
    """
    Display all pending articles awaiting editor approval.

    Restricts access to editors only and retrieves unapproved
    articles with related author and publisher information.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered pending articles page.
    """
    if request.user.role != "editor":
        messages.error(
            request,
            "Only editors can review pending articles.",
        )
        return redirect("home")

    articles = Article.objects.filter(
        approved=False
    ).select_related(
        "author",
        "publisher",
    ).order_by("-created_at")

    return render(
        request,
        "news/pending_articles.html",
        {"pending_articles": articles},
    )


@login_required
def approve_article(request, article_id):
    """
    Approve a pending article and notify subscribers.

    Marks the article as approved, records approval metadata,
    sends notification emails to subscribed readers, and
    redirects back to the pending articles list.

    Args:
        request (HttpRequest): Incoming HTTP request.
        article_id (int): ID of the article to approve.

    Returns:
        HttpResponse or HttpResponseRedirect: Rendered approval
        confirmation or redirect to pending articles.
    """
    if request.user.role != "editor":
        messages.error(
            request,
            "Only editors can approve articles.",
        )
        return redirect("home")

    article = get_object_or_404(
        Article,
        id=article_id,
        approved=False,
    )

    if request.method == "POST":
        article.approved = True
        article.approved_by = request.user
        article.approved_at = timezone.now()
        article.save()

        send_article_approval_email(article)

        messages.success(
            request,
            f'"{article.title}" has been approved.',
        )
        return redirect("pending_articles")

    return render(
        request,
        "news/approve_article.html",
        {"article": article},
    )


def send_article_approval_email(article):
    """
    Send email notifications to subscribers when an article is approved.

    Emails readers subscribed to the article's publisher and
    followers of the article's author.

    Args:
        article (Article): Approved article instance.

    Returns:
        None
    """
    publisher_subscribers = (
        article.publisher.subscribed_readers.all()
        if article.publisher
        else []
    )
    journalist_subscribers = article.author.journalist_followers.all()

    recipient_emails = {
        user.email
        for user in list(publisher_subscribers)
        + list(journalist_subscribers)
        if user.email
    }

    if not recipient_emails:
        return

    publisher_name = (
        article.publisher.name
        if article.publisher
        else "Independent"
    )

    subject = f"New approved article: {article.title}"
    message = (
        "Hello,\n\n"
        "A new article has been approved and published.\n\n"
        f"Title: {article.title}\n"
        f"Author: {article.author.username}\n"
        f"Publisher: {publisher_name}\n\n"
        f"Summary:\n{article.summary}\n\n"
        f"Content preview:\n{article.content[:300]}\n\n"
        "Thank you for subscribing."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=list(recipient_emails),
        fail_silently=False,
    )


class SubscribedArticleAPIView(APIView):
    """
    API endpoint returning approved articles for subscribed clients.

    Clients authenticate using an API key provided in the
    X-API-KEY request header. Articles returned match the
    publishers and journalists the client is subscribed to.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for subscribed articles.

        Args:
            request (Request): DRF request object.

        Returns:
            Response: JSON list of approved articles or
            an authentication error response.
        """
        api_key = request.headers.get("X-API-KEY")

        if not api_key:
            return Response(
                {"error": "API key is required in the X-API-KEY header."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            client = APIClientSubscription.objects.get(api_key=api_key)
        except APIClientSubscription.DoesNotExist:
            return Response(
                {"error": "Invalid API key."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        subscribed_publishers = client.subscribed_publishers.all()
        subscribed_journalists = client.subscribed_journalists.all()

        articles = Article.objects.filter(
            approved=True
        ).filter(
            Q(publisher__in=subscribed_publishers)
            | Q(author__in=subscribed_journalists)
        ).distinct().select_related(
            "author",
            "publisher",
            "approved_by",
        )

        serializer = ArticleSerializer(articles, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )