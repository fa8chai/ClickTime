from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User 
from profile.models import Default_username
from profile.models import Profile



class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        if extra_fields.get('is_staff') :
            raise ValueError('User must have is_staff=False')
        
        if extra_fields.get('is_superuser') :
            raise ValueError('User must have is_superuser=False')
        
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        user_profile, created = Profile.objects.get_or_create(user = user)
        user_profile.username = Default_username(email)
        user_profile.save()

        return user


    def create_superuser(self, email, password, **extra_fields):
        
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


        user_profile, created = Profile.objects.get_or_create(user = user)
        user_profile.username = Default_username(email)
        user_profile.email_confirmed = True
        user_profile.save()
        return user

    


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    objects = CustomUserManager()

    def __str__(self):
        return self.email



   