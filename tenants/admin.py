# tenants/admin.py
from django.contrib import admin, messages
from django.core.management import call_command
from django.core.mail import send_mail
from django.conf import settings
from django_tenants.admin import TenantAdminMixin

from .models import Client, Domain

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("name", "schema_name", "tenant_type", "created_on", "paid_until")
    list_filter = ("tenant_type", "on_trial")
    search_fields = ("name", "schema_name")
    ordering = ("-created_on",)

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)

        if is_new:
            obj.create_schema(check_if_exists=True, verbosity=1, sync_schema=False)

            call_command(
                "migrate_schemas",
                tenant=obj.schema_name,
                interactive=False,
                verbosity=1
            )

            if not obj.domains.exists():
                Domain.objects.create(
                    domain=f"{obj.schema_name}.localhost",
                    tenant=obj,
                    is_primary=True
                )

            # Κάνουμε setup (groups, admin χρήστη κλπ.)
            admin_email, admin_password = self.setup_initial_data(obj)

            # Προσθέτουμε Success Message
            messages.success(
                request,
                f"✅ Tenant '{obj.name}' δημιουργήθηκε! ➔ Admin login: {admin_email} / {admin_password}"
            )

    def setup_initial_data(self, tenant):
        """
        Δημιουργεί default group και superuser για το νέο tenant.
        Επιστρέφει email και password του admin.
        """
        from django_tenants.utils import schema_context
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group

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

                # Αν υπάρχει must_change_password στο μοντέλο
                if hasattr(user, "must_change_password"):
                    user.must_change_password = True
                    user.save()

                # Στέλνουμε Email με credentials
                self.send_admin_credentials(admin_email, admin_password)

            return admin_email, admin_password

    def send_admin_credentials(self, admin_email, admin_password):
        """
        Στέλνει email με τα credentials στον νέο Tenant Admin.
        """
        send_mail(
            subject="Καλωσορίσατε στο Digital Concierge!",
            message=(
                f"Τα στοιχεία πρόσβασης στο Control Panel σας είναι:\n\n"
                f"Email/Login: {admin_email}\n"
                f"Password: {admin_password}\n\n"
                f"Σας παρακαλούμε να αλλάξετε άμεσα τον κωδικό σας μετά το πρώτο login.\n"
                f"Καλή συνέχεια!"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=True,
        )
