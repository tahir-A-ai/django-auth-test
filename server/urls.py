from django.contrib import admin
from django.urls import path, include
from accounts.urls import auth_patterns
from accounts.views import MyProfileView, EditProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include(auth_patterns)),
    path('api/my-profile/', MyProfileView.as_view(), name='my_profile'),
    path('api/edit-profile/', EditProfileView.as_view(), name='edit_profile'),
]