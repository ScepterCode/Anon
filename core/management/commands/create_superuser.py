"""
Command to initialize the application with a superuser
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a superuser for admin access'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin')
        parser.add_argument('--email', type=str, default='admin@example.com')
        parser.add_argument('--password', type=str, default='admin123')

    def handle(self, *args, **options):  # noqa: ARG002
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(  # noqa: E501
                self.style.WARNING(f'User "{username}" already exists')  # type: ignore
            )
            return

        User.objects.create_superuser(username, email, password)
        self.stdout.write(  # noqa: E501
            self.style.SUCCESS(f'Successfully created superuser "{username}"')  # type: ignore
        )
