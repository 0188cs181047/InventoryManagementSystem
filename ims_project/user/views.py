from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
# from .forms import RegisterForm, LoginForm
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import reverse


# import logging

# logger = logging.getLogger('myproject.custom')


def home(request):
    # logger.info("This is home")
    return render(request , "user/home.html")



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


from django.contrib.auth import logout

@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        login_url = reverse('login')  
        return Response({
            "message": "User registered successfully",
            "redirect_url": login_url 
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def logout_api(request):
    logout(request)
    return redirect('home')

class TokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            return redirect('home')  
        return response
