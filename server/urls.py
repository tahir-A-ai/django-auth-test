from django.contrib import admin
from django.urls import path, include
from accounts.urls import auth_patterns
from accounts.views import MyProfileView, EditProfileView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="ServerProject API",
      default_version='v1',
      description="API documentation for ServerProject",
      terms_of_service="https://www.serverproject.local/terms-of-service/",
      contact=openapi.Contact(email="contact@serverproject.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include(auth_patterns)),
    path('api/my-profile/', MyProfileView.as_view(), name='my_profile'),
    path('api/edit-profile/', EditProfileView.as_view(), name='edit_profile'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]