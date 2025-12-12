from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Post, Comment

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['nickname', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff']
    search_fields = ['nickname', 'email', 'first_name', 'last_name']
    ordering = ['nickname']
    
    fieldsets = (
        (None, {'fields': ('nickname', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nickname', 'email', 'first_name', 'last_name', 'date_of_birth', 'password1', 'password2'),
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'category', 'text_preview', 'created_at', 'total_likes']
    search_fields = ['text', 'author__nickname']
    list_filter = ['category', 'created_at']
    date_hierarchy = 'created_at'
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'text_preview', 'created_at', 'total_likes']
    search_fields = ['text', 'author__nickname']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'