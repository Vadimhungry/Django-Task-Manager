from django.test import TestCase, Client
from django.urls import reverse
from .views import UserCreate, UserUpdateFormView, UserDelete
from .forms import UserCreationForm, CustomUserCreationForm
from django.contrib.auth import get_user_model
import json
from django.utils.translation import gettext as _
from django.contrib.messages import get_messages


class TestCreateUser(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.client = Client()
        with open('task_manager/fixtures/test_data.json', 'r') as f:
            data = json.load(f)
            self.new_user = data.get('users').get('new')

    def test_create_user(self):
        response = self.client.get(reverse("users_index"))
        self.assertNotContains(
            response,
            f"{self.new_user['first_name']} {self.new_user['last_name']}"
        )

        response = self.client.get(reverse("user_create"))
        self.assertIsInstance(response.context["form"], UserCreationForm)
        self.assertIs(
            response.resolver_match.func.view_class,
            UserCreate
        )

        response = self.client.post(reverse("user_create"), self.new_user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("user_login"))

        response = self.client.get(reverse("users_index"))
        self.assertContains(
            response,
            f"{self.new_user['first_name']} {self.new_user['last_name']}"
        )


class TestUpdateUser(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(username="Alpha")
        with open('task_manager/fixtures/test_data.json', 'r') as f:
            data = json.load(f)
            self.new_user = data.get('users').get('updated')
        self.url = reverse("user_update", kwargs={"pk": self.user.id})

    def test_update_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            self.url,
            reverse("user_update", kwargs={"pk": self.user.id})
        )
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)

        self.client.force_login(self.user)
        response = self.client.post(self.url, self.new_user)

        self.assertEquals(
            self.url,
            reverse("user_update", kwargs={"pk": self.user.id})
        )
        self.assertRedirects(response, reverse("users_index"), 302)
        self.assertEqual(response["Location"], reverse("users_index"))
        self.assertIs(
            response.resolver_match.func.view_class,
            UserUpdateFormView
        )

        response = self.client.get(reverse("users_index"))

        self.assertContains(
            response,
            f"{self.new_user['first_name']} {self.new_user['last_name']}"
        )


class TestDeleteUser(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.client = Client()

    def test_delete_users(self):
        del_user = get_user_model().objects.get(username="Beta")
        response = self.client.get(
            reverse("delete_user", kwargs={"pk": del_user.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertIs(
            response.resolver_match.func.view_class,
            UserDelete
        )

        self.client.force_login(del_user)
        response = self.client.post(
            reverse("delete_user", kwargs={"pk": del_user.id})
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("users_index"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[1]),
            _("The user has been successfully deleted")
        )
