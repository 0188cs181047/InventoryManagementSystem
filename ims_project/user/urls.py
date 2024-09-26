from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/register/', views.register_api, name='register_api'),
    path('api/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', views.read_users_api, name='read_users_api'),
    path('logout/', views.logout_api, name='logout'),
    path('ims/user/update/<int:item_id>/', views.update_ims_user, name='update_ims_user'),
    path('ims/user/delete/<int:item_id>/', views.delete_ims_user, name='delete_item'),
    
]



