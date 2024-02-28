from django.test import TestCase, Client
from django.urls import reverse
from .views import UserCreateFormView, UserUpdateFormView, UserDeleteFormView
from .forms import UserCreationForm, CustomUserCreationForm
from django.contrib.auth import get_user_model

class TestCreateUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.new_user = {
            "first_name": "Natasha",
            "last_name": "Noga",
            "username": "New",
            "password1": "QwertySuperP@ssword3",
            "password2": "QwertySuperP@ssword3"}

    def test_create_user(self):
        response = self.client.get(reverse("users_index"))
        self.assertNotContains(response, "Natasha Noga")

        response = self.client.get(reverse("user_create"))
        self.assertEquals(reverse("user_create"), '/users/create/')
        self.assertIsInstance(response.context['form'], UserCreationForm)
        self.assertIs(
            response.resolver_match.func.view_class,
            UserCreateFormView
        )

        response = self.client.post(reverse("user_create"), self.new_user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/login/")

        response = self.client.get(reverse('users_index'))
        self.assertContains(response, "Natasha Noga")


class TestUpdateUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = get_user_model().objects.get(username="Alpha")
        self.new_user = {
            "username": "Updated",
            "first_name": "Ulyana",
            "last_name": "Umina",
            "password1": "2QwertySuperP@ssword3",
            "password2": "2QwertySuperP@ssword3"
        }
        self.url = reverse("user_update", kwargs={"user_id": self.user.id})

    def test_update_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.url, f"/users/{self.user.id}/update/")
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

        self.client.force_login(self.user)
        response = self.client.post(self.url, self.new_user)

        self.assertEquals(self.url, f"/users/{self.user.pk}/update/")
        self.assertRedirects(response, reverse("users_index"), 302)
        self.assertEqual(response['Location'], "/users/")
        self.assertIs(
            response.resolver_match.func.view_class,
            UserUpdateFormView
        )

        response = self.client.get(reverse("users_index"))
        self.assertContains(response, "Ulyana Umina")


class TestDeleteUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()

    def test_delete_users(self):
        del_user = \
            get_user_model().objects.get(username="Beta")
        response = self.client.get(
            reverse(
                "delete_user",
                kwargs={"user_id": del_user.id}
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertIs(
            response.resolver_match.func.view_class,
            UserDeleteFormView
        )
        self.assertEqual(response['Location'], "/users/")

        self.client.force_login(del_user)
        response = self.client.post(
            reverse(
                "delete_user",
                kwargs={"user_id": del_user.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertIs(
            response.resolver_match.func.view_class,
            UserDeleteFormView
        )
        self.assertEqual(response['Location'], "/users/")
        self.assertFalse(
            get_user_model().objects.filter(username="Beta").exists()
                         )