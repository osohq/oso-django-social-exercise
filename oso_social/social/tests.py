from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from .models import Post, User


class Step0(TestCase):
    fixtures = ['social-oso.yaml']

    def test_get_all_posts(self):
        """Test that no authorization is applied, and all posts are returned."""
        response = self.client.get(reverse("index"))
        self.assertQuerysetEqual(
            response.context["posts"],
            [8, 7, 6, 5, 4, 3, 2, 1],
            transform=lambda p: p.id
        )

class Step1(TestCase):
    fixtures = ['social-oso.yaml']

    def test_get_all_posts(self):
        """Test that no authorization is applied, and all posts are returned."""
        response = self.client.get(reverse("index"))
        self.assertQuerysetEqual(
            response.context["posts"],
            [],
            transform=lambda p: p.id
        )

        # Admins can see everything.
        self.client.login(username='superuser_admin', password='superuser')
        response = self.client.get(reverse("index"))
        self.assertQuerysetEqual(
            response.context["posts"],
            [8, 7, 6, 5, 4, 3, 2, 1],
            transform=lambda p: p.id
        )

class Step2(TestCase):
    fixtures = ['social-step2.yaml']
    def test_get_all_posts(self):
        """Test that no authorization is applied, and all posts are returned."""
        # Admins can see everything.
        self.client.login(username='superuser_admin', password='superuser')
        response = self.client.get(reverse("index"))
        self.assertQuerysetEqual(
            response.context["posts"],
            [5, 4, 3, 2, 1],
            transform=lambda p: p.id
        )

    def test_get_group_posts(self):
        """Test that group member sees only groups posts."""
        response = self.client.get(reverse("list_group", args=(1,)))
        self.client.login(username='user', password='user')
        self.assertQuerysetEqual(
            response.context["posts"],
            [],
            transform=lambda p: p.id
        )

        self.client.login(username='bowler', password='bowler')
        response = self.client.get(reverse("list_group", args=(1,)))
        self.assertQuerysetEqual(
            response.context["posts"],
            [5],
            transform=lambda p: p.id
        )

class Step3(Step2):
    def test_create_post_group(self):
        """Test that new posts are only allowed for groups the user is in."""
        # New post no group allowed.
        self.client.login(username='bowler', password='bowler')
        response = self.client.post('/new/', {'contents': 'ok post', 'access_level': 0})
        self.assertEqual(response.status_code, 302)

        # New post group user is in allowed.
        response = self.client.post('/new/', {'contents': 'ok post', 'access_level': 0, 'group': 1})
        self.assertEqual(response.status_code, 302)

        # New post group user is not in rejected.
        response = self.client.post('/new/', {'contents': 'ok post', 'access_level': 0, 'group': 2})
        self.assertEqual(response.status_code, 403)

class Step4(Step3): pass
