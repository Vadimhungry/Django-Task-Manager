from django.test import TestCase, Client
from django.urls import reverse
from .views import UserCreate, UserDelete
from .forms import UserCreationForm, CustomUserCreationForm
from django.contrib.auth import get_user_model
from ..utils import get_fixture_data
from django.utils.translation import gettext as _
from .models import CustomUser
from ..settings import FIXTURE_PATH
import os


class TestCreateUser(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.client = Client()
        data = get_fixture_data(os.path.join(FIXTURE_PATH, 'test_data.json'))
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

        response = self.client.post(
            reverse("user_create"),
            self.new_user,
            follow=True
        )
        self.assertContains(
            response,
            _("The user has been successfully registered")
        )

        response = self.client.get(reverse("users_index"))
        self.assertContains(
            response,
            f"{self.new_user['first_name']} {self.new_user['last_name']}"
        )


class TestUpdateUser(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(username="Alpha")
        self.another_user = get_user_model().objects.get(username="Beta")
        data = get_fixture_data(os.path.join(FIXTURE_PATH, 'test_data.json'))
        self.new_user = data.get('users').get('updated')
        self.url = reverse("user_update", kwargs={"pk": self.user.id})
        self.another_url = reverse("user_update", kwargs={"pk": self.another_user.id})

    def test_update_user_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            self.url,
            reverse("user_update", kwargs={"pk": self.user.id})
        )
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)

        self.client.force_login(self.user)
        response = self.client.post(
            self.url,
            self.new_user,
            follow=True
        )
        self.assertContains(
            response,
            _("User changed successfully")
        )
        response = self.client.get(reverse("users_index"))
        self.assertContains(
            response,
            f"{self.new_user['first_name']} {self.new_user['last_name']}"
        )

    def test_update_user_failure(self):

        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(
            self.url,
            self.another_url
        )
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)
        self.client.force_login(self.user)
        response = self.client.post(
            self.another_url,
            self.new_user,
            follow=True
        )
        self.assertContains(
            response,
            _("You do not have permission to change another user.")
        )


class TestDeleteUser(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.client = Client()

    def test_delete_user_success(self):
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
            reverse("delete_user", kwargs={"pk": del_user.id}),
            follow=True
        )
        self.assertContains(
            response,
            _("The user has been successfully deleted")
        )

        self.assertFalse(CustomUser.objects.filter(username="Beta").exists())

    def test_delete_user_failure(self):
        del_user = get_user_model().objects.first()
        another_user = get_user_model().objects.last()
        response = self.client.get(
            reverse("delete_user", kwargs={"pk": del_user.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertIs(
            response.resolver_match.func.view_class,
            UserDelete
        )

        self.client.force_login(another_user)
        response = self.client.post(
            reverse("delete_user", kwargs={"pk": del_user.id}),
            follow=True
        )
        self.assertContains(
            response,
            _("You do not have permission to change another user.")
        )
        self.assertTrue(get_user_model().objects.filter(id=del_user.id).exists())
