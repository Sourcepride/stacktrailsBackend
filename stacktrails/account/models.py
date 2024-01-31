from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.utils import timezone

# Create your models here.
from .manager import CustomManager
from utils.model_helpers import create_uid


class User(AbstractBaseUser,  PermissionsMixin):
    uid = models.CharField(max_length=20, unique=True, default=create_uid)
    first_name = models.CharField(max_length=120, null=True, blank=False)
    last_name = models.CharField(max_length=120, null=True, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        pass

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"