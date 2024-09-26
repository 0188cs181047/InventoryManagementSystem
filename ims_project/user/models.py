from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
import logging
logger = logging.getLogger('custom_logger')

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            logger.info("User Must Have a Username")
            raise ValueError('Users must have a username')
        if not email:  # Check for empty email
            logger.info("User Must Have an Email Address")
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.save(using=self._db)
        return user

class IMSUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(verbose_name="email", max_length=255, unique=True)
    password = models.CharField(max_length=255)
    re_enterpass = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # User is active or not
    is_staff = models.BooleanField(default=False)   # User can log into admin site
    is_superuser = models.BooleanField(default=False) # User is superuser

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Add a custom related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Add a custom related name
        blank=True
    )

    def __str__(self):
        return self.username
