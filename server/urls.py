from django.contrib import admin
from django.urls import path, include
# from accounts.urls import auth_patterns
from accounts.views import MyProfileView, EditProfileView
from .swagger import schema_view
from .swagger import swagger_urlpatterns

urlpatterns = [
   path('admin/', admin.site.urls),
   path("api/", include("accounts.urls"))
]
urlpatterns += swagger_urlpatterns