from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('users/<int:id>/', users, name='users'),
    path('user/<int:pk>/', user_detail, name='user_detail'),
    path('user-role/<int:id>/', get_user_role, name='get_user_role'),
]

