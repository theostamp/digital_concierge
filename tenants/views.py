# backend/tenants/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tenants.models import Client, Domain
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

class TenantListView(APIView):
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

class TenantDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        tenant = get_object_or_404(Client, pk=pk)
        domain = Domain.objects.filter(tenant=tenant).first()

        return Response({
            "id": tenant.id,
            "name": tenant.name,
            "schema_name": tenant.schema_name,
            "domain_url": domain.domain if domain else "—"
        })

class TenantCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get("name")
        schema_name = request.data.get("schema_name")
        domain_url = request.data.get("domain_url", f"{schema_name}.localhost")

        if not name or not schema_name:
            return Response({"error": "Missing name or schema_name"}, status=400)

        tenant = Client.objects.create(name=name, schema_name=schema_name)
        Domain.objects.create(domain=domain_url, tenant=tenant, is_primary=True)

        return Response({"id": tenant.id}, status=status.HTTP_201_CREATED)
