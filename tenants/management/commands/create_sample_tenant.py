# backend/tenants/management/commands/create_sample_tenant.py

from django.core.management.base import BaseCommand
from tenants.models import Client, Domain

class Command(BaseCommand):
    help = "Creates a sample tenant for testing purposes."

    def handle(self, *args, **options):
        name = "Sample Tenant"
        schema_name = "sample"
        domain_url = "sample.localhost"

        if Client.objects.filter(schema_name=schema_name).exists():
            self.stdout.write(self.style.WARNING(f"Tenant '{schema_name}' already exists."))
            return

        tenant = Client.objects.create(name=name, schema_name=schema_name)
        Domain.objects.create(domain=domain_url, tenant=tenant, is_primary=True)

        self.stdout.write(self.style.SUCCESS(f"Successfully created tenant '{name}' with schema '{schema_name}' and domain '{domain_url}'."))
