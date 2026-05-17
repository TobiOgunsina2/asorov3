from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager, Role
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
