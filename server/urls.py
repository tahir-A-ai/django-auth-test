from django.contrib import admin
from django.urls import path, include
from accounts.urls import auth_patterns, user_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include((auth_patterns))),
    path('api/user/', include((user_patterns))),
]