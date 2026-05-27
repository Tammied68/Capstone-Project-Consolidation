from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("reader-dashboard/", views.reader_dashboard, name="reader_dashboard"),
    path("journalist-dashboard/", views.journalist_dashboard, name="journalist_dashboard"),
    path("editor-dashboard/", views.editor_dashboard, name="editor_dashboard"),
    path("articles/create/", views.create_article, name="create_article"),
    path("articles/pending/", views.pending_articles, name="pending_articles"),
    path(
        "articles/<int:article_id>/approve/",
        views.approve_article,
        name="approve_article",
    ),
]