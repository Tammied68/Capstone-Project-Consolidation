from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from news.models import Article, Newsletter


class Command(BaseCommand):
    help = "Create default groups and assign permissions."

    def handle(self, *args, **options):
        reader_group, _ = Group.objects.get_or_create(name="Reader")
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        journalist_group, _ = Group.objects.get_or_create(name="Journalist")

        # Clear existing permissions so the command can be run safely again.
        reader_group.permissions.clear()
        editor_group.permissions.clear()
        journalist_group.permissions.clear()

        # Article permissions
        view_article = Permission.objects.get(
            codename="view_article",
            content_type__app_label=Article._meta.app_label,
            content_type__model=Article._meta.model_name,
        )
        add_article = Permission.objects.get(
            codename="add_article",
            content_type__app_label=Article._meta.app_label,
            content_type__model=Article._meta.model_name,
        )
        change_article = Permission.objects.get(
            codename="change_article",
            content_type__app_label=Article._meta.app_label,
            content_type__model=Article._meta.model_name,
        )
        delete_article = Permission.objects.get(
            codename="delete_article",
            content_type__app_label=Article._meta.app_label,
            content_type__model=Article._meta.model_name,
        )
        approve_article = Permission.objects.get(
            codename="can_approve_article",
            content_type__app_label=Article._meta.app_label,
            content_type__model=Article._meta.model_name,
        )

        # Newsletter permissions
        view_newsletter = Permission.objects.get(
            codename="view_newsletter",
            content_type__app_label=Newsletter._meta.app_label,
            content_type__model=Newsletter._meta.model_name,
        )
        add_newsletter = Permission.objects.get(
            codename="add_newsletter",
            content_type__app_label=Newsletter._meta.app_label,
            content_type__model=Newsletter._meta.model_name,
        )
        change_newsletter = Permission.objects.get(
            codename="change_newsletter",
            content_type__app_label=Newsletter._meta.app_label,
            content_type__model=Newsletter._meta.model_name,
        )
        delete_newsletter = Permission.objects.get(
            codename="delete_newsletter",
            content_type__app_label=Newsletter._meta.app_label,
            content_type__model=Newsletter._meta.model_name,
        )

        # Reader permissions
        reader_group.permissions.add(
            view_article,
            view_newsletter,
        )

        # Editor permissions
        editor_group.permissions.add(
            view_article,
            change_article,
            delete_article,
            approve_article,
            view_newsletter,
            change_newsletter,
            delete_newsletter,
        )

        # Journalist permissions
        journalist_group.permissions.add(
            add_article,
            view_article,
            change_article,
            delete_article,
            add_newsletter,
            view_newsletter,
            change_newsletter,
            delete_newsletter,
        )

        self.stdout.write(self.style.SUCCESS("Groups and permissions set up successfully."))
