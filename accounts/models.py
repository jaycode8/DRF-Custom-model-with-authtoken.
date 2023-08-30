from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# lets create the manager for the users model

class UsersManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Super user must have is_staff=True")
        if not extra_fields.get('is_superuser'):
            raise ValueError('Super user must have is_superuser=True')
        return self.create_user(email, password, **extra_fields)



class Users(AbstractBaseUser):
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'other')
    )
    _id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128, null=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender'] #----- email and password are required already by default when creating superuserso no need to add them

    objects = UsersManager()

    
    def __str__(self):
        return self.email

    #---- this lines will enable loging in as admin to display admin site
    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

