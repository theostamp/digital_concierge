# 📁 tenants/management/commands/tenant_shell.py

from django.core.management.base import BaseCommand
from django_tenants.utils import get_tenant_model, schema_context
from django.db import connection

class Command(BaseCommand):
    help = "Launch Django shell for a specific tenant."

    def add_arguments(self, parser):
        parser.add_argument('--schema', type=str, help='Tenant schema name')

    def handle(self, *args, **options):
        schema_name = options['schema']

        if not schema_name:
            self.stderr.write(self.style.ERROR('Παρακαλώ δώστε --schema=όνομα_σχήματος'))
            return

        tenant_model = get_tenant_model()
        try:
            tenant = tenant_model.objects.get(schema_name=schema_name)
        except tenant_model.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'Ο tenant με schema "{schema_name}" δεν βρέθηκε.'))
            return

        self.stdout.write(self.style.SUCCESS(f'✅ Εκτέλεση shell για tenant: {tenant.schema_name}'))

        with schema_context(schema_name):
            from django.core.management import call_command
            call_command('shell')
