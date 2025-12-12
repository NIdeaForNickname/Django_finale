from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.png')
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='forum_users',
        related_query_name='forum_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='forum_users',
        related_query_name='forum_user',
    )
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    def save(self, *args, **kwargs):
        if self.nickname:
            self.username = self.nickname
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nickname or self.username

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True, default='category_icons/default.png')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.nickname} - {self.text[:50]}"
    
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.author.nickname} - {self.text[:50]}"
    
    def total_likes(self):
        return self.likes.count()