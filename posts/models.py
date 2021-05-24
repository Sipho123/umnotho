from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
# Create your models here.

class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(Profile, default=None, related_name='likes')
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name ='posts')
    #body = models.TextField()
    def _str_(self):
        return str(self.body)[:30]

   

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comment_set.all().count()         
       

    def get_posts_no(self):
        return self

    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return str(self.pk)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),

)

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

