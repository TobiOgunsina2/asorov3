from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import UserRole, Role
from django.conf import settings
from .enums import RoleName

ROLE_TO_GROUP = {
    RoleName.CONTENT_CREATOR: 'ContentArchitect',
    RoleName.REVIEWER:        'Reviewer',
}

# ── Assign default role on registration ───────────────────

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_default_role(sender, instance, created, **kwargs):
    if not created:
        return
    try:
        learner_role = Role.objects.get(name=RoleName.LEARNER)
    except Role.DoesNotExist:
        return  # migrations haven't seeded roles yet — safe to skip
    UserRole.objects.create(user=instance, role=learner_role, granted_by=None)

# ── Sync UserRole → Django Group ──────────────────────────


@receiver(post_save, sender=UserRole)
def sync_role_to_group(sender, instance, **kwargs):
    group_name = ROLE_TO_GROUP.get(instance.role.name)
    if not group_name:
        return
    group, _ = Group.objects.get_or_create(name=group_name)
    if instance.is_active and instance.is_valid():
        instance.user.groups.add(group)
    else:
        instance.user.groups.remove(group)