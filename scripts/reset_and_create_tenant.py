# scripts/reset_and_create_tenant.py

from django.db import connection
from tenants.models import Client, Domain
import os

# ----------- SETTINGS -----------
NEW_SCHEMA_NAME = 'test1'
NEW_TENANT_NAME = 'Test Tenant 1'
NEW_DOMAIN = 'test1.localhost'

# ----------- FUNCTIONS -----------

def drop_schema(schema_name):
    with connection.cursor() as cursor:
        print(f"\n[+] Dropping schema '{schema_name}'...")
        cursor.execute(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE;')

def recreate_public_schema():
    with connection.cursor() as cursor:
        print("\n[+] Recreating 'public' schema...")
        cursor.execute('DROP SCHEMA IF EXISTS public CASCADE;')
        cursor.execute('CREATE SCHEMA public;')
        cursor.execute('GRANT ALL ON SCHEMA public TO public;')
        cursor.execute('GRANT ALL ON SCHEMA public TO concierge_user;')

# ----------- SCRIPT EXECUTION -----------

print("\n================ RESET START ================")

# 1. Clean everything
recreate_public_schema()

# 2. Make fresh migrations
print("\n[+] Making migrations...")
os.system('python manage.py makemigrations tenants')
os.system('python manage.py makemigrations buildings')
os.system('python manage.py makemigrations users')
os.system('python manage.py makemigrations announcements')
os.system('python manage.py makemigrations votes')
os.system('python manage.py makemigrations user_requests')

# 3. Apply shared/public migrations
print("\n[+] Applying shared migrations...")
os.system('python manage.py migrate_schemas --shared')

# 4. Clean any tenants left (from the old public)
print("\n[+] Deleting existing tenants...")
try:
    Client.objects.all().delete()
except Exception as e:
    print(f"[!] No tenants to delete or error: {e}")

# 5. Create new tenant
print(f"\n[+] Creating new tenant '{NEW_SCHEMA_NAME}'...")
tenant = Client(
    schema_name=NEW_SCHEMA_NAME,
    name=NEW_TENANT_NAME,
    paid_until='2030-12-31',
    on_trial=True,
)
tenant.save()

# 6. Attach a domain
print(f"\n[+] Creating domain '{NEW_DOMAIN}'...")
domain = Domain()
domain.domain = NEW_DOMAIN
domain.tenant = tenant
domain.is_primary = True
domain.save()

print("\n================ RESET COMPLETE ✅ ================")
print(f"\nAccess your tenant at: http://{NEW_DOMAIN}:8000\n")
