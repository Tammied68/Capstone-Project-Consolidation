from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):

    """
    Custom user model for the News application.

    Extends Django's AbstractUser to support role-based behavior
    (reader, editor, journalist) and content subscriptions.

    Fields:
        role (str): The user's role in the system.
        publisher (Publisher): Publisher this user belongs to (if applicable).
        subscribed_publishers (ManyToMany): Publishers followed by the user.
        subscribed_journalists (ManyToMany): Journalists followed by the user.
    """

    class Role(models.TextChoices):
        READER = "reader", "Reader"
        EDITOR = "editor", "Editor"
        JOURNALIST = "journalist", "Journalist"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.READER,
    )

    publisher = models.ForeignKey(
        "news.Publisher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff_members",
        help_text="Publisher linked to this editor or journalist.",
    )

    subscribed_publishers = models.ManyToManyField(
        "news.Publisher",
        blank=True,
        related_name="subscribed_readers",
        help_text="Publishers followed by a reader.",
    )

    subscribed_journalists = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="journalist_followers",
        limit_choices_to={"role": "journalist"},
        help_text="Journalists followed by a reader.",
    )

    def clean(self):
        super().clean()

        if self.role == self.Role.READER and self.publisher is not None:
            raise ValidationError("Readers should not be assigned to a publisher.")

    def assign_role_group(self):
        """
        Place the user in the correct Django group based on role.
        Remove the user from other role groups first.
        """
        role_to_group = {
            self.Role.READER: "Reader",
            self.Role.EDITOR: "Editor",
            self.Role.JOURNALIST: "Journalist",
        }

        target_group_name = role_to_group.get(self.role)
        if not target_group_name:
            return

        role_group_names = ["Reader", "Editor", "Journalist"]
        self.groups.remove(*Group.objects.filter(name__in=role_group_names))

        target_group = Group.objects.filter(name=target_group_name).first()
        if target_group:
            self.groups.add(target_group)

    def save(self, *args, **kwargs):
        """
        Ensure role-specific fields stay sensible and assign groups.
        """
        if self.role == self.Role.READER:
            self.publisher = None

        super().save(*args, **kwargs)
        self.assign_role_group()

    @property
    def is_reader(self):
        return self.role == self.Role.READER

    @property
    def is_editor(self):
        return self.role == self.Role.EDITOR

    @property
    def is_journalist(self):
        return self.role == self.Role.JOURNALIST

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
