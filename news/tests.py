from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import APIClientSubscription, Article, Publisher


class SubscribedArticleAPITestCase(APITestCase):
    def setUp(self):
        """
        Set up test data for API subscription tests.
        """
        self.User = get_user_model()

        # Create publisher
        self.publisher = Publisher.objects.create(
            name="Daily Times",
            description="Daily news publisher",
            website="https://dailytimes.example.com",
        )

        self.other_publisher = Publisher.objects.create(
            name="Global News",
            description="Global news publisher",
            website="https://globalnews.example.com",
        )

        # Create journalists
        self.journalist_1 = self.User.objects.create_user(
            username="journalist1",
            password="testpass123",
            role="journalist",
            publisher=self.publisher,
        )

        self.journalist_2 = self.User.objects.create_user(
            username="journalist2",
            password="testpass123",
            role="journalist",
            publisher=self.other_publisher,
        )

        # Create approved and unapproved articles
        self.article_1 = Article.objects.create(
            title="Approved Article from Subscribed Publisher",
            summary="Summary 1",
            content="Content 1",
            author=self.journalist_1,
            publisher=self.publisher,
            approved=True,
        )

        self.article_2 = Article.objects.create(
            title="Unapproved Article from Subscribed Publisher",
            summary="Summary 2",
            content="Content 2",
            author=self.journalist_1,
            publisher=self.publisher,
            approved=False,
        )

        self.article_3 = Article.objects.create(
            title="Approved Article from Unsubscribed Publisher",
            summary="Summary 3",
            content="Content 3",
            author=self.journalist_2,
            publisher=self.other_publisher,
            approved=True,
        )

        self.article_4 = Article.objects.create(
            title="Approved Independent Article by Subscribed Journalist",
            summary="Summary 4",
            content="Content 4",
            author=self.journalist_1,
            publisher=None,
            approved=True,
        )

        # Create API client subscription
        self.api_client = APIClientSubscription.objects.create(
            client_name="Test Client",
            api_key="test-api-key-123",
        )
        self.api_client.subscribed_publishers.add(self.publisher)
        self.api_client.subscribed_journalists.add(self.journalist_1)

        self.url = reverse("subscribed_articles_api")

    def test_api_returns_articles_for_valid_api_key(self):
        """
        The API should return approved articles from subscribed
        publishers or subscribed journalists.
        """
        response = self.client.get(
            self.url,
            HTTP_X_API_KEY="test-api-key-123",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        returned_titles = [article["title"] for article in response.data]
        self.assertIn("Approved Article from Subscribed Publisher", returned_titles)
        self.assertIn(
            "Approved Independent Article by Subscribed Journalist",
            returned_titles,
        )

    def test_api_rejects_missing_api_key(self):
        """
        The API should reject requests that do not include an API key.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["error"],
            "API key is required in the X-API-KEY header.",
        )

    def test_api_rejects_invalid_api_key(self):
        """
        The API should reject requests with an invalid API key.
        """
        response = self.client.get(
            self.url,
            HTTP_X_API_KEY="invalid-key",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid API key.")

    def test_api_excludes_unapproved_articles(self):
        """
        Unapproved articles should not be returned even if the client
        is subscribed to the publisher or journalist.
        """
        response = self.client.get(
            self.url,
            HTTP_X_API_KEY="test-api-key-123",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        returned_titles = [article["title"] for article in response.data]
        self.assertNotIn(
            "Unapproved Article from Subscribed Publisher",
            returned_titles,
        )

    def test_api_excludes_unsubscribed_articles(self):
        """
        Approved articles from unsubscribed publishers and journalists
        should not be returned.
        """
        response = self.client.get(
            self.url,
            HTTP_X_API_KEY="test-api-key-123",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        returned_titles = [article["title"] for article in response.data]
        self.assertNotIn(
            "Approved Article from Unsubscribed Publisher",
            returned_titles,
        )