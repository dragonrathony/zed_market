from django.db import models
from categories.models import Category


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Post(models.Model):

    # additional
    blog_title = models.CharField(max_length=100, null=True)
    blog_category = models.CharField(max_length=100, null=True)
    blog = models.CharField(max_length=1000, null=True)
    blog_img = models.ImageField(null=True)


    def __str__(self):
        return self.blog_title