from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:nickname>/', views.user_profile, name='user_profile'),
    
    path('category/create/', views.create_category, name='create_category'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/like/', views.toggle_post_like, name='toggle_post_like'),
    
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:pk>/like/', views.toggle_comment_like, name='toggle_comment_like'),
]