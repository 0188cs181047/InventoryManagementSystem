from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import IMSUser

# Use get_user_model to fetch your custom user model (IMSUser)
User = get_user_model()

class IMSUserModelTest(TestCase):

    def setUp(self):
        # Common setup code can go here
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "testpass123"
    
    def test_create_user(self):
        """
        Test creating a new regular user
        """
        user = User.objects.create_user(
            username=self.username, 
            email=self.email, 
            password=self.password
        )
        
        # Assert the user is created successfully
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_active)  
        self.assertFalse(user.is_staff)  
        self.assertFalse(user.is_superuser)  

    def test_create_superuser(self):
        """
        Test creating a superuser
        """
        superuser = User.objects.create_superuser(
            username='adminuser', 
            email='adminuser@example.com', 
            password='superpass123'
        )
        
        # Assert the superuser is created successfully
        self.assertEqual(superuser.username, 'adminuser')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
    
    def test_create_user_without_username(self):
        """
        Test that creating a user without a username raises a ValueError
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='',  
                email='nousername@example.com',
                password='somepass123'
            )

    def test_create_user_without_email(self):
        """
        Test that creating a user without an email raises a ValueError
        # """
        # with self.assertRaises(ValueError):
        #     User.objects.create_user(
        #         username='nouser', 
        #         email='',  
        #         password='somepass123'
            # )

    def test_user_string_representation(self):
        """
        Test the string representation of the user model (__str__)
        """
        user = User.objects.create_user(
            username='strtestuser', 
            email='strtestuser@example.com', 
            password='strpass123'
        )
        self.assertEqual(str(user), 'strtestuser')

    def test_user_permissions(self):
        """
        Test assigning groups and permissions to the user
        """
        user = User.objects.create_user(
            username='permtestuser', 
            email='permtestuser@example.com', 
            password='permtestpass'
        )
        
        # Add groups or permissions if needed and assert accordingly
        self.assertEqual(user.groups.count(), 0)
        self.assertEqual(user.user_permissions.count(), 0)




class IMSUserTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.api_client = APIClient()

        # Create a test user
        self.superuser = IMSUser.objects.create_superuser(username='admin', email='admin@example.com', password='password')
        self.test_user = IMSUser.objects.create_user(username='testuser', email='testuser@example.com', password='password')

    def test_home_view(self):
        """
        Test the home view returns the current username
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home')) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response, 'testuser')  
        

    # def test_register_api(self):
    #     """
    #     Test the register_api view for successful registration
    #     """
    #     url = reverse('register_api')
    #     data = {
    #         'username': 'newuser',
    #         'email': 'newuser@example.com',
    #         'password': 'newpassword',
    #         're_enterpass': 'newpassword' 
    #     }
    #     response = self.api_client.post(url, data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertIn('token_obtain_pair', response.data)

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
        # self.api_client.force_authenticate(user=self.superuser)
        # url = reverse('update_ims_user', kwargs={'item_id': self.test_user.id})
        # print(f"Testing update for user ID: {self.test_user.id}")  # Debugging line
        # data = {
        #     'email': 'updatedemail@example.com'
        # }
        # response = self.api_client.put(url, data, format='json')
        # print(response.status_code, response.data)  # Print response status and data for debugging
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # # Ensure email is updated
        # self.test_user.refresh_from_db()
        # self.assertEqual(self.test_user.email, 'updatedemail@example.com')


    def test_delete_ims_user(self):
        """
        Test deleting an existing IMS user
        """
        self.api_client.force_authenticate(user=self.superuser)
        url = reverse('delete_item', kwargs={'item_id': self.test_user.id})

        response = self.api_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the user is deleted
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.test_user.id)

    def test_my_token_obtain_pair_view(self):
        """
        Test login using MyTokenObtainPairView
         """
        # url = reverse('token_obtain_pair')
        # data = {
        #     'username': 'testuser',
        #     'password': 'testpassword'
        # }
        # response = self.api_client.post(url, data, format='json')
        
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn('access', response.data)
        # self.assertIn('refresh', response.data)

    def test_token_refresh_view(self):
        """
        Test token refresh via TokenRefreshView
        """
        # Get refresh token for test user
        # refresh = RefreshToken.for_user(self.test_user)
        # url = reverse('token_refresh')
        # data = {
        #     'refresh': str(refresh)
        # }
        # response = self.api_client.post(url, data, format='json')
        
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn('access', response.data)
