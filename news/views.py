from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    approved_articles = Article.objects.filter(approved=True).order_by("-created_at")
    context = {
        "approved_articles": approved_articles,
    }
    return render(request, "news/reader_dashboard.html", context)


@login_required
def journalist_dashboard(request):
    my_articles = Article.objects.filter(author=request.user).order_by("-created_at")
    context = {
        "my_articles": my_articles,
    }
    return render(request, "news/journalist_dashboard.html", context)


@login_required
def editor_dashboard(request):
    pending_articles = Article.objects.filter(approved=False).order_by("-created_at")
    context = {
        "pending_articles": pending_articles,
    }
    return render(request, "news/editor_dashboard.html", context)


@login_required
def create_article(request):
    if request.user.role != "journalist":
        messages.error(request, "Only journalists can create articles.")
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

    return render(request, "news/create_article.html", {"form": form})


@login_required
def pending_articles(request):
    if request.user.role != "editor":
        messages.error(request, "Only editors can review pending articles.")
        return redirect("home")

    articles = Article.objects.filter(approved=False).select_related(
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
    if request.user.role != "editor":
        messages.error(request, "Only editors can approve articles.")
        return redirect("home")

    article = get_object_or_404(Article, id=article_id, approved=False)

    if request.method == "POST":
        article.approved = True
        article.approved_by = request.user
        article.approved_at = timezone.now()
        article.save()

        messages.success(request, f'"{article.title}" has been approved.')
        return redirect("pending_articles")

    return render(
        request,
        "news/approve_article.html",
        {"article": article},
    )


class SubscribedArticleAPIView(APIView):
    """
    Return approved articles for the publishers and journalists
    that the API client is subscribed to.
    The client must send its API key in the X-API-KEY header.
    """

    def get(self, request, *args, **kwargs):
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
        ).distinct().select_related("author", "publisher", "approved_by")

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
