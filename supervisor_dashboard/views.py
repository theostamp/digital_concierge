from django.core.paginator import Paginator

# μέσα στη dashboard_view:
tenants = Client.objects.all()

if query:
    tenants = tenants.filter(name__icontains=query)

if status_filter:
    tenants = tenants.filter(...)

paginator = Paginator(tenants, 10)  # 10 tenants ανά σελίδα
page_number = request.GET.get('page')
tenants = paginator.get_page(page_number)

# Στο context:
"tenants": tenants
"paginator": paginator,
"page_number": page_number,
