from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignUpView, LoginView, MyProfileView, EditProfileView

urlpatterns = [
    path('auth/sign-up/', SignUpView.as_view(), name='sign_up'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', MyProfileView.as_view(), name='my_profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
]