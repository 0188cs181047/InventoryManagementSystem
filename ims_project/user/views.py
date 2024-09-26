from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import login as auth_login, authenticate,logout
from django.contrib import messages
# from .forms import RegisterForm, LoginForm
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import reverse

import logging
from functools import wraps
from .serializers import RegisterSerializer
from .models import IMSUser

# Get the logger
# logger = logging.getLogger('custom_logger')





# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Registration successful. Please log in.')
#             return redirect('login')
#         else:
#             messages.error(request, 'Registration failed. Please correct the errors.')
#     else:
#         form = RegisterForm()

#     return render(request, 'user/register.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 auth_login(request, user)
#                 return redirect('home')  # Redirect to home or dashboard page
#             else:
#                 messages.error(request, 'Invalid username or password.')
#         else:
#             messages.error(request, 'Invalid form data.')
#     else:
#         form = LoginForm()

#     return render(request, 'user/login.html', {'form': form})


from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import IMSUser  # Import your custom IMSUser model
import logging

logger = logging.getLogger("my_app_logger")

def home(request):
    try:
        # Fetch the current logged-in user
        current_user = request.user

        # Check if the current user is an instance of IMSUser or the default User model
        if isinstance(current_user, IMSUser):
            current_username = current_user.username  # Fetch IMSUser username
            logger.debug(f"IMSUser Logged in: {current_username}")
            
        else:
            current_username = current_user.username  # Fetch default User username
            logger.debug(f"User Logged in: {current_username}")
        
        return render(request, "user/home.html", context={"username": current_username})
    
    except Exception as e:
        logger.error(f"Error occurred in home view: {str(e)}")
        return render(request, "user/error.html", {"message": "An error occurred."})




@api_view(['POST'])
def register_api(request):
    try:
        if request.method == "POST":  # Check if the request is POST
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                logger.info("Successful Register")
                serializer.save()
                login_url = reverse('token_obtain_pair')  
                return Response({
                    "message": "User registered successfully",
                    "login_url": login_url 
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid request method."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        logger.error(e)


@api_view(['GET'])
def read_users_api(request):
    try:
        if not request.user.is_authenticated:
            logger.error("Authentication error")
            return Response({"error": "Authentication required."}, status=status.HTTP_403_FORBIDDEN)
        superusers = IMSUser.objects.all()
        logger.info("Read The All Registered User")
        

        serializer = RegisterSerializer(superusers, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)


@api_view(['PUT'])
def update_ims_user(request, item_id):
    try:
        item = IMSUser.objects.get(id=item_id)
        logger.debug("Get User Data")
    except IMSUser.DoesNotExist:
        logger.error("User Not Found")
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = RegisterSerializer(item, data=request.data, partial=True)  
    if serializer.is_valid():
        serializer.save()
        logger.info("Updated User Data")
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_ims_user(request, item_id):
    try:
        item = IMSUser.objects.get(id=item_id)
        logger.info("Deleted The User Data")
    except IMSUser.DoesNotExist as e:
        logger.error(e)
        return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
    item.delete()
    return Response({"message": "Item deleted successfully."}, status=status.HTTP_200_OK)

def logout_api(request):
    try:
        logout(request)
        logger.info("Logout Successully")
        return redirect('home')
    except Exception as e:
        logger.error(e)


user_dct = {}
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        print(f"========={username} ==={password}")

        user_dct["username"] = username
        user_dct["password"] = password

        user = authenticate(username=username, password=password)
        
        print("================",user)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            # auth_login(request, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        
        
        elif user is None:
            ims_data = IMSUser.objects.get(username= username)
            print(ims_data, ims_data.password)
            print("inside elig-----------")
            refresh = RefreshToken.for_user(ims_data)
            # auth_login(request, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)




class TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            username = user_dct["username"]
            password = user_dct["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')

            try:
                ims_user = IMSUser.objects.get(username=username)

                # Authenticate IMSUser by checking password manually
                if ims_user.check_password(password):
                    auth_login(request, ims_user)  # Log in IMSUser
                    return redirect('home')
                else:
                    return HttpResponse("Invalid credentials for IMSUser", status=401)
            
            except IMSUser.DoesNotExist:
                # If IMSUser also doesn't exist, return error response
                return HttpResponse("Invalid credentials", status=401)


             
        return response


