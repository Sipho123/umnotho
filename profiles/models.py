from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.shortcuts import reverse

# Create your models here.

class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(qs)
        print("#########")

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)
        print("#########")

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        print("#########")
        return available
        

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

class Profile(models.Model):
    user = models.CharField(max_length=200,blank=True)
    username = models.CharField(max_length=200,blank=True)
    business_name =  models.CharField(max_length=200,blank=True)
    headline = models.CharField(max_length=1000)
    industry = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    country = models.CharField(max_length=200, null=True, blank=True)
    province = models.CharField(max_length=200,null=True, blank=True)
    surburb_township = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    Manucipality = models.CharField(max_length=1000)
    email = models.EmailField(max_length=200,null=True, blank=True)
    cell = models.IntegerField(null=True)
    land_line = models.IntegerField(null=True)
    fax_number = models.IntegerField(null=True)
    code = models.IntegerField(null=True)
    contact_person = models.CharField(max_length=1000)
    business_established_date = models.DateTimeField(auto_now=True)
    bio = models.TextField(default="no bio...",
                           max_length=300, blank=True)
    CEO = models.CharField(max_length=1000)
    email_address = models.EmailField(max_length=254, )
    first_name = models.CharField(max_length=200,null=True, blank=True)
    last_name = models.CharField(max_length=200,null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    # intall pillow -after insetting an avatar img in media_root folder
    #create media_root inside static_cdn
    #find avatar.png on line
    connections = models.ManyToManyField(
        User, blank=True, related_name='connections')
    slug = models.SlugField(unique=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to='uploads/')

    following = models.ManyToManyField(User, related_name='following',blank=True)
    #website = models.URLField(max_length=200, **options)

    objects = ProfileManager()

    def _str_(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%y')}"

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})
            
    def get_connections(self):
        return self.connections.all()

    def get_connections_no(self):
        return self.connections.all().count()

    def get_posts_no(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value=='Like':
                total_liked += 1
            return total_liked


    def get_likes_recieved_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name
    

    def save(self, *args, **kwargs):
        ex = False
        if self.username:
            to_slug = slugify(str(self.username) + "")
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + "" + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=200,blank=True)
    user = models.CharField(max_length=200,blank=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"




    def profiles_posts(self):
        return self.post_set.all()

    def __str__(self):
        return str(self.user)
    
    
    class Meta:
        ordering = ('-created',)
