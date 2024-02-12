from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.conf import settings


# Create your models here.
from .manager import CustomManager
from .choices import SocialChoices
from utils.model_helpers import create_uid
from utils.helpers import inmemory_wrapper


class User(AbstractBaseUser, PermissionsMixin):
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
        indexes = [models.Index(fields=("email",), name="email_idx")]

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self):
        if not self.first_name and not self.last_name:
            return self.email
        return f"{self.first_name} {self.last_name}"


class SocialAccount(models.Model):
    avatar = models.URLField(null=True, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
        related_name="socials",
        related_query_name="social",
    )
    social_id = models.CharField(max_length=30, null=False, unique=True)
    provider = models.CharField(
        max_length=20, null=False, blank=False, choices=SocialChoices.choices
    )

    class Meta:
        indexes = [models.Index(fields=("social_id",), name="social_idx")]


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        related_query_name="profile",
    )
    cover_image = models.ImageField(
        upload_to="images/cover/",
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )
    image = models.ImageField(
        upload_to="images/profile/",
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )
    avatar = models.URLField(null=True, blank=False)
    bio = models.TextField(default="")

    class Meta:
        indexes = [models.Index(fields=("id",), name="id_idx")]

    def save(self, *args, **kwargs):
        self.image = inmemory_wrapper(self.image)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user
