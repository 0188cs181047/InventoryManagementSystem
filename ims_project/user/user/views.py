from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

# Fetch the custom user model
User = get_user_model()

class IMSUserTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.api_client = APIClient()

        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

        # Create superuser for `read_users_api`
        self.superuser = User.objects.create_superuser(
            username='adminuser',
            email='adminuser@example.com',
            password='adminpassword'
        )

    def test_home_view(self):
        """
        Test the home view returns the current username
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))  # Assuming you named the path 'home'
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'testuser')  # Check if the username is in the response

    def test_register_api(self):
        """
        Test the register_api view for successful registration
        """
        url = reverse('register_api')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            're_enterpass': 'newpassword'  # Match the field name in your serializer
        }
        response = self.api_client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('login_url', response.data)  # Check if login URL is returned

    def test_read_users_api(self):
        """
        Test the read_users_api view to fetch all users
        """
        self.api_client.force_authenticate(user=self.superuser)
        url = reverse('read_users_api')

        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check if it returns both users (superuser and test_user)

    def test_update_ims_user(self):
        """
        Test updating an existing IMS user
        """
        self.api_client.force_authenticate(user=self.superuser)
        url = reverse('update_ims_user', kwargs={'item_id': self.test_user.id})
        data = {
            'email': 'updatedemail@example.com'
        }
        response = self.api_client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure email is updated
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.email, 'updatedemail@example.com')

    def test_delete_ims_user(self):
        """
        Test deleting an existing IMS user
        """
        self.api_client.force_authenticate(user=self.superuser)
        url = reverse('delete_ims_user', kwargs={'item_id': self.test_user.id})

        response = self.api_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the user is deleted
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.test_user.id)

    def test_my_token_obtain_pair_view(self):
        """
        Test login using MyTokenObtainPairView
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.api_client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh_view(self):
        """
        Test token refresh via TokenRefreshView
        """
        # Get refresh token for test user
        refresh = RefreshToken.for_user(self.test_user)
        url = reverse('token_refresh')
        data = {
            'refresh': str(refresh)
        }
        response = self.api_client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
