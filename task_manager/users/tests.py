from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

# Create your tests here.
class TestUsers(TestCase):

    def setUp(self):
        self.client = Client()
    def test_index(self):
        response = self.client.get('/users/')
        response.status_code
        self.assertEqual(response.status_code, 200)

    def test_user_create_get(self):
        response = self.client.get('/users/create/')
        response.status_code
        self.assertEqual(response.status_code, 200)

    def test_user_create_post(self):
        valid_form_data = {
            'first_name': 'Ivan',
            'last_name': 'Durak',
            'username': 'testuser',
            'password1': 'Testpassword12345',
            'password2': 'Testpassword12345',
        }

        # Send a POST request with valid form data
        response = self.client.post(reverse("user_create"), valid_form_data)

        # Check if the response redirects to the 'user_login' URL
        self.assertRedirects(response, reverse('user_login'), status_code=302)

    def test_user_login(self):
        login_url = reverse("user_login")

        login_data = {
            'username': 'testuser',
            'password': 'Testpassword12345',
        }

        # Send a POST request to the login view with credentials
        response = self.client.post(login_url, data=login_data, follow=True)
        self.assertRedirects(response, reverse_lazy("index"), status_code=302)

