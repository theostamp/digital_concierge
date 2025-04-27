# supervisor_dashboard/admin.py
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path, reverse
from tenants.models import Client
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
import openpyxl
from io import BytesIO

def save_virtual_workbook(wb):
    virtual_workbook = BytesIO()
    wb.save(virtual_workbook)
    return virtual_workbook.getvalue()

class SupervisorAdminSite(admin.AdminSite):
    site_header = "Ψηφιακός Θυρωρός - Supervisor Panel"
    site_title = "Supervisor Admin"
    index_title = "Καλωσορίσατε στο Supervisor Panel"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='supervisor-dashboard'),
            path('extend_trial/<int:tenant_id>/', self.admin_view(self.extend_trial), name='extend-trial'),
            path('deactivate_tenant/<int:tenant_id>/', self.admin_view(self.deactivate_tenant), name='deactivate-tenant'),
            path('export_tenants/', self.admin_view(self.export_tenants), name='export-tenants'),
        ]
        return custom_urls + urls
        
    def each_context(self, request):
        context = super().each_context(request)
        from tenants.models import Client
        from django.utils import timezone
        from datetime import timedelta

        soon_to_expire_count = Client.objects.filter(
            on_trial=True,
            paid_until__lte=timezone.now() + timedelta(days=7)
        ).count()

        context['dashboard_url'] = "/admin/dashboard/"
        context['soon_to_expire_count'] = soon_to_expire_count
        return context


    def dashboard_view(self, request):
        query = request.GET.get('q')
        status_filter = request.GET.get('status')

        tenants = Client.objects.all()

        if query:
            tenants = tenants.filter(name__icontains=query)

        if status_filter == 'active':
            tenants = tenants.filter(on_trial=False)
        elif status_filter == 'trial':
            tenants = tenants.filter(on_trial=True)
        elif status_filter == 'inactive':
            tenants = tenants.filter(is_active=False)

        tenants_count = tenants.count()
        active_count = tenants.filter(on_trial=False).count()
        trial_count = tenants.filter(on_trial=True).count()
        recent_tenants = tenants.order_by('-created_on')[:5]

        soon_to_expire = tenants.filter(
            on_trial=True,
            paid_until__lte=timezone.now() + timedelta(days=7)
        )

        context = dict(
            self.each_context(request),
            tenants_count=tenants_count,
            active_count=active_count,
            trial_count=trial_count,
            recent_tenants=recent_tenants,
            soon_to_expire=soon_to_expire,
            tenants=tenants,                # για pagination
            search_query=query,
            status_filter=status_filter,
        )
        # **Αφαίρεσε** το current_app=… εδώ:
        return TemplateResponse(
            request,
            "supervisor_dashboard/dashboard.html",
            context
        )
    
    def extend_trial(self, request, tenant_id):
        tenant = Client.objects.get(pk=tenant_id)
        tenant.paid_until += timedelta(days=30)
        tenant.save()
        self.message_user(request, f"✅ Το Trial του {tenant.name} παρατάθηκε κατά 30 ημέρες.")
        return HttpResponseRedirect(reverse('supervisor-dashboard'))

    def deactivate_tenant(self, request, tenant_id):
        tenant = Client.objects.get(pk=tenant_id)
        tenant.is_active = False
        tenant.save()
        self.message_user(request, f"🚫 Ο Tenant {tenant.name} απενεργοποιήθηκε.")
        return HttpResponseRedirect(reverse('supervisor-dashboard'))

    def export_tenants(self, request):
        tenants = Client.objects.all()

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Tenants"

        ws.append(["Όνομα", "Schema", "Email", "Ημερομηνία Δημιουργίας", "Κατάσταση Trial", "Λήξη Trial"])

        for tenant in tenants:
            ws.append([
                tenant.name,
                tenant.schema_name,
                tenant.email if hasattr(tenant, 'email') else "",
                tenant.created_on.strftime('%d/%m/%Y') if tenant.created_on else "",
                "Ναι" if tenant.on_trial else "Όχι",
                tenant.paid_until.strftime('%d/%m/%Y') if tenant.paid_until else "",
            ])

        response = HttpResponse(
            content=save_virtual_workbook(wb),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="tenants.xlsx"'
        return response


# 👉 Ορισμός του custom admin site
supervisor_admin_site = SupervisorAdminSite(name='supervisor_dashboard')

supervisor_admin_site.register(Client)
