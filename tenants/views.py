# tenants/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from tenants.models import Client, Domain

class TenantListView(APIView):
    permission_classes = [IsAuthenticated]  # ή AllowAny για δοκιμές

    def get(self, request):
        tenants = Client.objects.all().order_by("name")
        domains = Domain.objects.select_related("tenant").all()
        domain_map = {d.tenant_id: d.domain for d in domains}

        data = [
            {
                "id": tenant.id,
                "name": tenant.name,
                "schema_name": tenant.schema_name,
                "domain_url": domain_map.get(tenant.id, "—"),
            }
            for tenant in tenants
        ]
        return Response(data)
