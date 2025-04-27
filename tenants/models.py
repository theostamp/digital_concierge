# tenants\models.py
from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    schema_name = models.CharField(max_length=63, unique=True)
    tenant_type = models.CharField(
        max_length=50,
        choices=[('management_office', 'Management Office'), ('other', 'Other')],
        default='management_office'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    paid_until = models.DateTimeField(null=True, blank=True)
    on_trial = models.BooleanField(default=False)   # Αν είναι trial ή paid
    auto_create_schema = True  # Αν θέλεις να δημιουργεί schema αυτόματα
    # Αν θέλεις να δημιουργεί schema αυτόματα, αλλιώς το κάνεις χειροκίνητα
    # με την εντολή `create_custom_tenant` που φτιάξαμε παραπάνω
    # Required
    auto_create_schema = True

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass  # Το μόνο πεδίο που έχει ήδη: `domain` (π.χ. subdomain.εταιρεία.gr)
