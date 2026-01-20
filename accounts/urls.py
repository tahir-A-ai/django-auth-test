from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SignUpView, LoginView, 
    MyProfileView, EditProfileView,
    UploadProfileImageView, DeleteProfileImageView,
    )

urlpatterns = [
    path('auth/sign-up/', SignUpView.as_view(), name='sign_up'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', MyProfileView.as_view(), name='my_profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('upload-image/', UploadProfileImageView.as_view(), name='upload-image'),
    path('delete-image/', DeleteProfileImageView.as_view(), name='delete-image'),
]