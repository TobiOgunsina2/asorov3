from django.db import migrations
from apps.users.enums import RoleName

# !!! Important: This migration should be run after the initial migration that creates the Role model.
# This migration seeds the Role model with predefined roles from RoleName enum.

def seed_roles(apps, schema_editor):
    Role = apps.get_model('users', 'Role')
    for value, label in RoleName.choices:
        Role.objects.get_or_create(name=value)


def unseed_roles(apps, schema_editor):
    Role = apps.get_model('users', 'Role')
    Role.objects.filter(name__in=RoleName.values).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),  # make sure this matches your last migration
    ]

    operations = [
        migrations.RunPython(seed_roles, unseed_roles),
    ]