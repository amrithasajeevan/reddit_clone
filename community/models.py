from django.db import models
from accounts.models import CustomUser
# Create your models here.

class Community(models.Model):
    community_name=models.CharField(max_length=100)
    image=models.FileField(upload_to="community_image")
    content=models.TextField(null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="c_user")
    followers = models.ManyToManyField("self", blank=True)
    
    
    def __str__(self):
        return self.community_name

    @property
    def followers_count(self):
        return self.followers.all().count()

