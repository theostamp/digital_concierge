from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tenants.models import Client
from django_tenants.utils import schema_context

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser for a specific tenant (schema)'

    def add_arguments(self, parser):
        parser.add_argument('--schema', type=str, required=True, help='Schema name of the tenant')
        parser.add_argument('--email', type=str, required=True, help='Superuser email')
        parser.add_argument('--password', type=str, required=True, help='Superuser password')
        parser.add_argument('--username', type=str, help='Optional username (default: email)')

    def handle(self, *args, **options):
        schema_name = options['schema']
        email = options['email']
        password = options['password']
        username = options['username'] or email

        try:
            if not Client.objects.filter(schema_name=schema_name).exists():
                self.stdout.write(self.style.ERROR(f"Tenant schema '{schema_name}' not found."))
                return

        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Tenant schema '{schema_name}' not found."))
            return

        with schema_context(schema_name):
            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f"User with email '{email}' already exists in schema '{schema_name}'."))
                return

            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created for schema '{schema_name}'."))