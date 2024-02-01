from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# from django.utils.encoding import python_2_unicode_compatible
# from django.utils.translation import ugettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('not-specified', 'Not specified')
    )
    
    phone=models.IntegerField(null=True)
    date_of_birth=models.DateField(null=True)
    profile_image = models.ImageField(null=True)
    website = models.URLField(null=True)
    bio = models.TextField(null=True)
    gender = models.CharField(max_length=80, choices=GENDER_CHOICES, null=True)
    followers = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", blank=True)
    push_token = models.TextField(default='')
    
    def __str__(self):
        return self.username

    @property
    def post_count(self):
        return self.images.all().count()

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
        return self.following.all().count()