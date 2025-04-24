from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from buildings.models import Building
from tenants.models import Client


class Command(BaseCommand):
    help = 'Create a building inside a specific tenant schema'

    def add_arguments(self, parser):
        parser.add_argument('--schema', type=str, required=True, help='Tenant schema name (e.g. etairia1)')
        parser.add_argument('--code', type=str, required=True, help='Unique code for the building (e.g. KOD123)')
        parser.add_argument('--name', type=str, required=True, help='Building name or description')
        parser.add_argument('--address', type=str, required=False, default='', help='Full street address')
        parser.add_argument('--city', type=str, required=False, default='', help='City')
        parser.add_argument('--postal', type=str, required=False, default='', help='Postal code')

    def handle(self, *args, **options):
        schema_name = options['schema']

        if not Client.objects.filter(schema_name=schema_name).exists():
            self.stdout.write(self.style.ERROR(f"Schema '{schema_name}' does not exist."))
            return

        with schema_context(schema_name):
            if Building.objects.filter(code=options['code']).exists():
                self.stdout.write(self.style.WARNING(f"Building with code '{options['code']}' already exists in schema '{schema_name}'."))
                return

            building = Building.objects.create(
                code=options['code'],
                name=options['name'],
                address=options['address'],
                city=options['city'],
                postal_code=options['postal']
            )

            self.stdout.write(self.style.SUCCESS(f"Building '{building.name}' (code: {building.code}) created successfully in schema '{schema_name}'."))
