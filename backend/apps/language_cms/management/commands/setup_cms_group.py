"""
language_cms/management/commands/setup_cms_group.py

Run: python manage.py setup_cms_group

Creates the 'ContentArchitect' group used to gate CMS access.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Creates the ContentArchitect group for CMS access control'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='ContentArchitect')
        if created:
            self.stdout.write(self.style.SUCCESS("✓ Created 'ContentArchitect' group"))
        else:
            self.stdout.write("  'ContentArchitect' group already exists")

        self.stdout.write(
            "\nTo grant a user access to the CMS, add them to this group:\n"
            "  user.groups.add(Group.objects.get(name='ContentArchitect'))\n"
            "or via Django Admin → Users → [user] → Groups."
        )
