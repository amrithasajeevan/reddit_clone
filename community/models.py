from django.db import models
from accounts.models import CustomUser
# Create your models here.

class Community(models.Model):
    community_name=models.CharField(max_length=100)
    image=models.FileField(upload_to="community_image")
    content=models.TextField(null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="c_user")
    followers = models.ManyToManyField(CustomUser, related_name="communities_following", blank=True)
    
    
    def __str__(self):
        return self.community_name

    @property
    def followers_count(self):
        return self.followers.all().count()
    

# class CommunityPost(models.Model):
#     community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="posts")
#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     image = models.FileField(upload_to="community_posts",null=True)
#     caption = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Post by {self.author.username} in {self.community.community_name}"

class CommunityPost(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.FileField(upload_to="community_posts",null=True)
    caption = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(CustomUser,related_name='likes')

# class Like(models.Model):
#     post = models.ManyToManyField(CommunityPost, related_name='likes')
#     creator = models.ManyToManyField(CustomUser, related_name='likes')
    

class Comment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)