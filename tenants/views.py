# tenants/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from tenants.models import Client, Domain
from rest_framework import status
from django.shortcuts import get_object_or_404

class TenantListView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]


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

    def post(self, request):
        name = request.data.get("name")
        schema_name = request.data.get("schema_name")

        if not name or not schema_name:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        tenant = Client.objects.create(name=name, schema_name=schema_name)
        Domain.objects.create(domain=f"{schema_name}.localhost", tenant=tenant, is_primary=True)

        return Response({"message": "Tenant created."}, status=status.HTTP_201_CREATED)


class TenantDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tenant_id):
        tenant = get_object_or_404(Client, id=tenant_id)
        domain = Domain.objects.filter(tenant=tenant).first()

        data = {
            "id": tenant.id,
            "name": tenant.name,
            "schema_name": tenant.schema_name,
            "domain_url": domain.domain if domain else "—",
        }
        return Response(data)
