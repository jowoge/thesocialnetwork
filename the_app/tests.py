from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from .models_factories import *
from rest_framework.test import APIClient
from rest_framework import status

# I wrote this code
class AppUserTests(TestCase):
    def test_app_user_creation(self):
        app_user = AppUserFactory()
        self.assertTrue(isinstance(app_user, AppUser))
        self.assertTrue(isinstance(app_user.user, User))
        self.assertEqual(AppUser.objects.count(), 1)

class PostsTests(TestCase):
    def test_post_creation(self):
        post = PostsFactory()
        self.assertTrue(isinstance(post, Posts))
        self.assertTrue(isinstance(post.user, User))
        self.assertEqual(Posts.objects.count(), 1)

class AppUserUpdateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.app_user = AppUser.objects.create(user=self.user)

    def test_update_app_user_data(self):
        client = APIClient()
        client.login(username='testuser', password='testpassword')

        # define the updated data
        updated_data = {
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'dob': '1990-01-01', 
            # 'pfp': '',
        }

        # make a PATCH request to update the user data
        response = client.patch(f'/api/users/{self.app_user.pk}/', updated_data, format='json')

        # check if the update was successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # refresh the app_user instance to get the latest data from the database
        self.app_user.refresh_from_db()

        # check if the user data has been updated
        self.assertEqual(self.app_user.first_name, 'Updated First Name')
        self.assertEqual(self.app_user.last_name, 'Updated Last Name')
        self.assertEqual(str(self.app_user.dob), '1990-01-01')  # Ensure it's a string in the expected format
# end of code I wrote