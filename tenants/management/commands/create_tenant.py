# tenants/management/commands/create_tenant.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
from tenants.models import Client, Domain
from django_tenants.utils import schema_context
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Create a new tenant with schema, domain and admin user."

    def add_arguments(self, parser):
        parser.add_argument('schema_name', type=str, help='The schema name (and subdomain) for the new tenant.')

    def handle(self, *args, **kwargs):
        schema_name = kwargs['schema_name'].strip().lower()

        # Δημιουργία Client
        client = Client(
            schema_name=schema_name,
            name=schema_name,
            tenant_type="Management Office",  # Default τύπος tenant (προσαρμόζεται αν χρειάζεται)
            paid_until="2030-12-31",
            on_trial=False,
        )
        client.save()

        # Δημιουργία Schema
        client.create_schema(check_if_exists=True, verbosity=1, sync_schema=False)

        # Migration για το νέο schema
        call_command(
            "migrate_schemas",
            tenant=schema_name,
            interactive=False,
            verbosity=1
        )

        # Δημιουργία Domain
        Domain.objects.create(
            domain=f"{schema_name}.localhost",
            tenant=client,
            is_primary=True
        )

        # Δημιουργία Admin Χρήστη
        self.setup_initial_data(client)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Tenant '{schema_name}' δημιουργήθηκε επιτυχώς!\n"
            f"🌐 URL: http://{schema_name}.localhost:8000\n"
            f"🔑 Admin login: admin@{schema_name}.com / Tenant123!"
        ))

    def setup_initial_data(self, tenant):
        """
        Δημιουργεί default group και superuser για το νέο tenant.
        """
        user_model = get_user_model()

        with schema_context(tenant.schema_name):
            Group.objects.get_or_create(name='Tenant Admins')

            admin_email = f"admin@{tenant.schema_name}.com"
            admin_username = admin_email
            admin_password = "Tenant123!"

            if not user_model.objects.filter(email=admin_email).exists():
                user = user_model.objects.create_superuser(
                    email=admin_email,
                    username=admin_username,
                    password=admin_password,
                    first_name="Admin",
                    last_name="Tenant",
                    is_active=True,
                )

                if hasattr(user, "must_change_password"):
                    user.must_change_password = True
                    user.save()
