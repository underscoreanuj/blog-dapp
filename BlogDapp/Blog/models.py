from django.db import models
from django.utils import timezone

from Utils.constants import FREE, PLUS

# Create your models here.


class Blog(models.Model):

    BLOG_TYPES = [
        (FREE, 'Free'),
        (PLUS, 'Plus')
    ]

    blog_id = models.AutoField(primary_key=True)
    blog_type = models.CharField(
        max_length=1, choices=BLOG_TYPES, default=FREE)
    blog_title = models.TextField()
    blog_description = models.TextField()
    blog_content = models.TextField()
    blog_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return """
            {} : {}
        """.format(self.blog_title, self.blog_description)
