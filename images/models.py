from django.db import models
from accounts.models import *
from django.contrib.humanize.templatetags.humanize import naturaltime
# from taggit.managers import TaggableManager
# from imagekit.models import ProcessedImageField
# from imagekit.processors import Transpose


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Image(TimeStampedModel):
    """ Image Model """
    file=models.FileField(upload_to="posts",null=True)
    location = models.CharField(max_length=140)
    caption = models.TextField()
    creator = models.ForeignKey(
        CustomUser, null=True, on_delete=models.CASCADE, related_name='images'
    )
    # tags = TaggableManager()

    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def comment_count(self):
        return self.comments.all().count()

    @property
    def natural_time(self):
        return naturaltime(self.created_at)

    @property
    def is_vertical(self):
        # Note: Make sure you have 'file' attribute defined in your model
        if self.file.width < self.file.height:
            return True
        else:
            return False

    def __str__(self):
        return '{} - {}'.format(self.location, self.caption)

    class Meta:
        ordering = ['-created_at']


class Comment(TimeStampedModel):
    """ Comment Model """
    message = models.TextField()
    creator = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    image = models.ForeignKey(Image, null=True, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.message


class Like(TimeStampedModel):
    """ Like Model """
    creator = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, null=True, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return 'User: {} - Image Caption: {}'.format(self.creator.username, self.image.caption)
