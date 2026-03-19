from django.urls import path
from .views import (
    home,
    reader_dashboard,
    journalist_dashboard,
    editor_dashboard,
    create_article,
    pending_articles,
    approve_article,
    SubscribedArticleAPIView,
)

urlpatterns = [
    path("", home, name="home"),

    # Dashboards
    path("reader-dashboard/", reader_dashboard, name="reader_dashboard"),
    path("journalist-dashboard/", journalist_dashboard, name="journalist_dashboard"),
    path("editor-dashboard/", editor_dashboard, name="editor_dashboard"),

    # Article workflow
    path("articles/create/", create_article, name="create_article"),
    path("articles/pending/", pending_articles, name="pending_articles"),
    path("articles/<int:article_id>/approve/", approve_article, name="approve_article"),

    # API
    path(
        "api/subscribed-articles/",
        SubscribedArticleAPIView.as_view(),
        name="subscribed_articles_api",
    ),
]