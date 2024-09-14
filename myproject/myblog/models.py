from django.db import models
from django.contrib.auth.models import User, auth


class Userinfo(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='profile_pics/')
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.user.username  
class Posts(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank= True,null= True)
    post_image = models.ImageField(blank=True,null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.title
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'