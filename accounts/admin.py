from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, Wallet

class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        'id', 'email', 'username', 'name', 'phone', 
        'view_profile_link',
        'is_staff', 'is_active', 'date_joined', 'last_login'
    )
    
    list_filter = ('is_staff', 'is_active', 'date_joined', 'last_login')
    search_fields = ('email', 'username', 'name', 'phone')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': (
                'name', 'phone', 'address', 
                'profile_image',        
                'profile_image_preview'
            )
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'name', 'password1', 'password2', 'phone', 'address', 'profile_image',),
        }),
    )

    readonly_fields = ('last_login', 'date_joined', 'profile_image_preview')

    def view_profile_link(self, obj):
        if obj.profile_image:
            return format_html('<a href="{}" target="_blank">View Image</a>', obj.profile_image.url)
        return "-"
    view_profile_link.short_description = "Profile Image"

    def profile_image_preview(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return "No Image Uploaded"
    profile_image_preview.short_description = "Image URL (Cloudinary)"


admin.site.register(User, CustomUserAdmin)
admin.site.register(Wallet)