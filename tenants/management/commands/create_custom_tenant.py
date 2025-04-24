from django.core.management.base import BaseCommand
from tenants.models import Client, Domain
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Creates a new tenant (company) with domain'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, required=True, help='Company name')
        parser.add_argument('--schema', type=str, required=True, help='Tenant schema name (e.g. company1)')
        parser.add_argument('--domain_url', type=str, required=True, help='Domain or subdomain (e.g. company1.localhost)')
        parser.add_argument('--trial', action='store_true', help='Set trial mode for tenant')

    def handle(self, *args, **options):
        name = options['name']
        schema_name = options['schema']
        domain_url = options['domain_url']
        trial = options['trial']

        if Client.objects.filter(schema_name=schema_name).exists():
            self.stdout.write(self.style.ERROR(f"Schema '{schema_name}' already exists."))
            return

        client = Client(
            name=name,
            schema_name=schema_name,
            on_trial=trial,
            paid_until=None  # Μπορείς να προσθέσεις λογική εδώ
        )
        client.save()

        # Δημιουργία domain
        domain = Domain()
        domain.domain = domain_url
        domain.tenant = client
        domain.is_primary = True
        domain.save()

        # 🔧 Εδώ κάνουμε migrate το συγκεκριμένο schema
        call_command('migrate_schemas', schema_name=schema_name)

        self.stdout.write(self.style.SUCCESS(
            f"Tenant '{name}' created with domain '{domain_url}' and schema '{schema_name}' migrated."
        ))