from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.core.management import CommandError

# Command to help create a superuser with email instead of username, since the custom user model uses email as the USERNAME_FIELD
class Command(BaseCommand):
    help = 'Create a superuser with email instead of username'

    def handle(self, *args, **options):
        from apps.users.models import User

        email = input('Email: ').strip()
        if not email:
            raise CommandError('Email cannot be empty')

        if User.objects.filter(email=email).exists():
            raise CommandError(f'User with email {email} already exists')

        password = self._get_pass()

        user = User.objects.create_superuser(
            email=email,
            password=password,
        )

        self.stdout.write(self.style.SUCCESS(f'Superuser {email} created successfully'))

    def _get_pass(self):
        import getpass
        while True:
            password = getpass.getpass('Password: ')
            confirm  = getpass.getpass('Password (again): ')
            if password != confirm:
                self.stderr.write('Passwords do not match, try again')
                continue
            if not password:
                self.stderr.write('Password cannot be empty')
                continue
            return password