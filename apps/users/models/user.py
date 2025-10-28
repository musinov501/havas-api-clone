from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.models import BaseModel
from apps.users.managers.user import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
   
    email = models.EmailField(
        max_length=255, unique=True, null=True,
        blank=True, db_index=True
    )

    username = models.CharField(
        max_length=150, unique=True, null=True,
        blank=True, db_index=True
    )

    phone_number = models.CharField(
        max_length=17, unique=True, null=True,
        blank=True, db_index=True
    )

    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    middle_name = models.CharField(max_length=64, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number' 
    REQUIRED_FIELDS = [] 

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email'], name='users_email_idx'),
            models.Index(fields=['username'], name='users_username_idx'),
            models.Index(fields=['phone_number'], name='users_phone_idx')
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(email__isnull=False) |
                      models.Q(username__isnull=False) |
                      models.Q(phone_number__isnull=False),
                name='user_must_have_identifier'
            )
        ]

    @property
    def full_name(self):
        
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        if self.username:
            return self.username
        elif self.phone_number:
            return self.phone_number

        return self.email

    def get_tokens(self, access_lifetime=None, refresh_lifetime=None):
        refresh = RefreshToken.for_user(self)


        if access_lifetime:
            refresh.access_token.set_exp(lifetime=access_lifetime)
        if refresh_lifetime:
            refresh.set_exp(lifetime=refresh_lifetime)

        refresh['email'] = self.email
        refresh['username'] = self.username
        refresh['user_id'] = self.id

        expires_at = timezone.now() + timedelta(seconds=refresh.access_token.lifetime.total_seconds())
        refresh_expires_at = timezone.now() + timedelta(seconds=refresh.lifetime.total_seconds())

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'token_type': 'Bearer',
            'expires_at': expires_at.isoformat(),
            'refresh_expires_at': refresh_expires_at.isoformat(),
        }
