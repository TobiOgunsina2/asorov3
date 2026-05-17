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
            user.set_unusable_password()   # social-only users never get a password
        user.save(using=self._db)
        return user

    # ── public factories ──────────────────────────────────────────────
    def create_user(self, email, **extra):
        """Normal user (social login only)."""
        extra.setdefault("role", Role.USER)
        return self._create_user(email, role=extra.pop("role"), **extra)

    def create_reviewer(self, email, **extra):
        extra["role"] = Role.REVIEWER
        return self._create_user(email, **extra)

    def create_staff_user(self, email, password, **extra):
        extra["role"] = Role.STAFF
        return self._create_user(email, role=Role.STAFF, password=password, **extra)

    def create_superuser(self, email, password, **extra):
        extra["role"] = Role.SUPER
        return self._create_user(email, role=Role.SUPER, password=password,
                                  is_superuser=True, **extra)
