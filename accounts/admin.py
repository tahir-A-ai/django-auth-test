from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, Wallet
import cloudinary.uploader
import os

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
                'cloudinary_preview'
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

    readonly_fields = ('last_login', 'date_joined', 'cloudinary_preview')

    def view_profile_link(self, obj):
        if obj.cloudinary_url:
            return format_html('<a href="{}" target="_blank">View Image</a>', obj.cloudinary_url)
        return "-"
    view_profile_link.short_description = "Profile Image"

    def cloudinary_preview(self, obj):
        if obj.cloudinary_url:
            return format_html(
                '<a href="{}" target="_blank">{}</a>', 
                obj.cloudinary_url, 
                obj.cloudinary_url
            )
        return "No Cloudinary Upload"
    cloudinary_preview.short_description = "Cloudinary URL"


    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            Wallet.objects.get_or_create(user=obj, defaults={'balance': 0, 'currency': 'Gems'})
        if 'profile_image' in form.changed_data and obj.profile_image:
            try:
                local_path = obj.profile_image.path
                if os.path.exists(local_path):
                    upload_response = cloudinary.uploader.upload(
                    local_path,
                    folder="user_profiles"
                )
                obj.cloudinary_url = upload_response.get('secure_url')
                obj.cloudinary_public_id = upload_response.get('public_id')
                obj.save(update_fields=['cloudinary_url', 'cloudinary_public_id'])
            except Exception as e:
                print(f"Error uploading to Cloudinary: {e}")


class WalletAdmin(admin.ModelAdmin):
    fields = ('user_id_display', 'user', 'balance', 'currency', 'created_at', 'updated_at')
    readonly_fields = ('user_id_display', 'created_at', 'updated_at')
    list_display = ('user_id_display', 'user', 'balance', 'currency', 'created_at', 'updated_at')
    def user_id_display(self, obj):
        return obj.user.id
    user_id_display.short_description = 'User ID'


admin.site.register(User, CustomUserAdmin)
admin.site.register(Wallet, WalletAdmin)
