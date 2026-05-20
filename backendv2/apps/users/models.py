from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager, Role
from django.contrib.auth.validators import UnicodeUsernameValidator
import uuid

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email     = models.EmailField(unique=True)
    name      = models.CharField(max_length=255, blank=True)
    role      = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = []          # email is already USERNAME_FIELD

    objects = UserManager()

    # ── role helpers (use in views/serializers) ───────────────────────
    @property
    def is_staff(self):           # required by Django admin
        return self.role in (Role.STAFF, Role.SUPER)

    @property
    def is_normal_user(self):
        return self.role == Role.USER

    @property
    def is_reviewer(self):
        return self.role == Role.REVIEWER

    def __str__(self):
        return f"{self.email} ({self.role})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # Unique user display name
    display_name = models.CharField(
        unique=True,
        blank=True,
        max_length=20,
        validators=[UnicodeUsernameValidator()],
        help_text="Public handle or display name (letters, digits, Unicode, @/./+/-/_ allowed)"
    )
    avatar_url = models.URLField(blank=True)

    xp = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)

    def __str__(self):
        return f"Profile of {self.user.email}"
