# tenants\models.py
from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    # Required
    auto_create_schema = True

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass  # Το μόνο πεδίο που έχει ήδη: `domain` (π.χ. subdomain.εταιρεία.gr)
