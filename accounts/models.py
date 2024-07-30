from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        password=None,
    ):

        if not email:
            raise ValueError('The email address must be set')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.role = 'ADMIN'
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    SUBSCRIBER = 'SUBSCRIBER'
    AUTHOR = 'AUTHOR'
    ADMIN = 'ADMIN'

    ROLES_CHOICES = [
        (SUBSCRIBER, 'Subscriber role'),
        (AUTHOR, 'Author role'),
        (ADMIN, 'Admin role'),
    ]

    correct_email = RegexValidator(
        regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        message='Enter a valid email address.'
    )
    email = models.EmailField(unique=True, validators=[correct_email])
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLES_CHOICES, default=SUBSCRIBER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
