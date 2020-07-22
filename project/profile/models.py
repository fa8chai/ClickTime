from django.db import models
from django.conf import settings
import string
import random
from django.db.models.signals import post_save
from django.dispatch import receiver


CustomUser = settings.AUTH_USER_MODEL

# Create your models here.

def Default_username(email):
                email = email.split('@')[0]
                d_username = ''


                for c in email :
                    if c.isalnum():
                        d_username += c
                    else:
                        d_username += '_'
                if d_username[-1] is not '_':
                    d_username += '_'
                
                d_username += ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.choice(range(3,6))))
                
                while True:
                    if not Profile.objects.filter(username = d_username).exists():
                        break
                    else:
                        d_username +=  ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.choice(range(3,6))))

                return d_username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(unique=True,blank=False,max_length=30)
    bio = models.TextField(max_length=400, blank=True)
    picture = models.ImageField( upload_to='images/',blank=True,null=True)
    email_confirmed = models.BooleanField(default=False)
    
    def follow(self,following_user_id):
        userfollowing = UserFollowing.objects.create(user_id = self, following_user_id = following_user_id)
        userfollowing.save()

    def unfollow(self, following_user_id):
        userfollowing = self.following.get(following_user_id = following_user_id)
        userfollowing.delete()

    def block(self, blocking_user_id):
        userblocking = UserBlocking.objects.create(user_id = self, blocking_user_id = blocking_user_id)
        userblocking.save()

    def unblock(self, blocking_user_id):
        userblocking = self.blocking.get(blocking_user_id = blocking_user_id)
        userblocking.delete()

    
    def __str__(self):
        return self.username

    @property
    def picture_url(self):
        if self.picture:
            return self.picture.url
        else:
            return settings.MEDIA_URL+'/default.jpg'


class UserFollowing(models.Model):

    user_id = models.ForeignKey(Profile, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(Profile, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ("user_id", "following_user_id")
        ordering = ["-created"]
        

    def __str__(self):
        return f"{self.user_id.username} follows {self.following_user_id.username}"


class UserBlocking(models.Model):

    user_id = models.ForeignKey(Profile, related_name='blocking', on_delete=models.CASCADE)
    blocking_user_id = models.ForeignKey(Profile, related_name='blocked_by', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        unique_together = ("user_id", "blocking_user_id")
        ordering = ["-created"]
        

    def __str__(self):
        return f"{self.user_id.username} blocking {self.blocking_user_id.username}"


@receiver(post_save, sender=CustomUser)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.username = Default_username(instance.email)
    instance.profile.save()
