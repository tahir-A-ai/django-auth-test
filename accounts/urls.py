from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignUpView, LoginView, MyProfileView, EditProfileView

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('my-profile/', MyProfileView.as_view(), name='my_profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
]