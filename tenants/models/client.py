from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Client(TenantMixin):
    # Πεδία
    name = models.CharField(max_length=100)
    schema_name = models.CharField(max_length=63, unique=True)
    tenant_type = models.CharField(
        max_length=50,
        choices=[
            ('management_office', 'Management Office'),
            ('other', 'Other Client'),
        ],
        default='management_office'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)

class Domain(DomainMixin):
    pass
