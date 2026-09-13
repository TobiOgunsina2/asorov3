from django.contrib.auth.base_user import BaseUserManager
from django.db import models

class Role(models.TextChoices):
    USER     = "user",       "Normal User"
    REVIEWER = "reviewer",   "Reviewer"
    STAFF    = "staff",      "Staff"
    SUPER    = "superuser",  "Super User"


class UserManager(BaseUserManager):

    def _create_user(self, email, role, password=None, **extra):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # social-only users never get a password
        user.save(using=self._db)
        return user

    # ── public factories ──────────────────────────────────────────────
    def create_user(self, email, **extra):
        """Normal user (social login only)."""
        role = extra.pop("role", Role.USER)
        return self._create_user(email, role=role, **extra)

    def create_reviewer(self, email, **extra):
        role = extra.pop("role", Role.REVIEWER)
        return self._create_user(email, role=role, **extra)

    def create_staff_user(self, email, password=None, **extra):
        role = extra.pop("role", Role.STAFF)
        return self._create_user(email, role=role, password=password, **extra)

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_superuser", True)

        if extra.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Safely extract 'role' if present, default to Role.SUPER
        role = extra.pop("role", Role.SUPER)

        return self._create_user(
            email=email,
            role=role,
            password=password,
            **extra
        )