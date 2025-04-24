from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from tenants.models import Client
from buildings.models import Building


class Command(BaseCommand):
    help = 'List all buildings within a specific tenant schema'

    def add_arguments(self, parser):
        parser.add_argument('--schema', type=str, required=True, help='Tenant schema name (e.g. etairia1)')

    def handle(self, *args, **options):
        schema_name = options['schema']

        if not Client.objects.filter(schema_name=schema_name).exists():
            self.stdout.write(self.style.ERROR(f"Schema '{schema_name}' does not exist."))
            return

        with schema_context(schema_name):
            buildings = Building.objects.all()
            if not buildings.exists():
                self.stdout.write(self.style.WARNING(f"No buildings found in schema '{schema_name}'."))
                return

            self.stdout.write(self.style.SUCCESS(f"Buildings in schema '{schema_name}':"))
            for b in buildings:
                self.stdout.write(f" - {b.name} (Code: {b.code}, Address: {b.address}, City: {b.city})")
