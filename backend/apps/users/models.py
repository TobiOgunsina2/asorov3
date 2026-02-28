from django.db import models
from django.utils.functional import cached_property
from django.contrib.auth.models import AbstractUser
import uuid
from .enums import RoleName
from .manager import UserManager

# Create your models here.

"""
NOTEE !!! - 
    user.set_unusable_password()
    user.save()
in user creation view so that they can't use the pw

    if user.has_usable_password():
check at password reset 

"""

class User(AbstractUser):
    """
    Custom User model. 
    Regular users sign in via Third Party (AllAuth).
    Staff users have passwords for Django Admin.
    """

    # Use UUIDs for public-facing IDs
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Force Email to be unique and required - Users cannot login through more than 1 method
    email = models.EmailField(unique=True)

    # Auth Metadata
    # Helps you debug login issues (e.g., "google", "github", or "internal")
    auth_provider = models.CharField(max_length=50, default="email")

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @cached_property
    def role_names(self) -> set[str]:
        """Cached set of active role names for this request lifecycle."""
        return set(
            self.user_roles
                .filter(is_active=True)
                .select_related('role')
                .values_list('role__name', flat=True)
        )

    def has_role(self, *roles: str) -> bool:
        return bool(self.role_names & set(roles))

    @property
    def is_creator(self) -> bool:
        return self.has_role(Role.CONTENT_CREATOR)

    @property
    def is_reviewer(self) -> bool:
        return self.has_role(Role.REVIEWER)

    @property
    def is_learner(self) -> bool:
        return self.has_role(Role.LEARNER)

# In the app there are two types of staff - |Creators| and |Reviewers|
# A creator can create access course specific details - grammar, curriculum
# Reviewers are for the planned social expansion, they add 
# likes to user exercises/stories and review user speech exercises 

class Role(models.Model):
    """
    Canonical list of roles in the system.
    Seeded via a data migration, not created at runtime.
    """

    name = models.CharField(max_length=50, unique=True, choices=RoleName.choices)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()


class UserRole(models.Model):
    """
    Through table: assigns a role to a user with full audit trail.
    """
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role       = models.ForeignKey(Role, on_delete=models.PROTECT)
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='roles_granted')
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)  # optional: time-limited roles
    is_active  = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'role')

    def is_valid(self):
        from django.utils import timezone
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True