#!/bin/bash

# scripts/reset.sh

echo ""
echo "========================================="
echo "⚠️  WARNING: This will DELETE everything!"
echo "========================================="
echo ""

read -p "Are you sure you want to reset the database? (yes/no): " answer

if [[ "$answer" != "yes" ]]; then
  echo "❌ Reset cancelled."
  exit 1
fi

echo ""
echo "🚀 Starting full RESET process..."

# Step 0: Ensure docker compose is up
if ! docker compose ps | grep -q "web"; then
  echo ""
  echo "🔧 Starting docker compose services..."
  docker compose up -d
else
  echo ""
  echo "✅ Docker services already running."
fi

# Step 1: Makemigrations
echo ""
echo "🔄 Making fresh migrations..."
docker compose exec -T web bash -c "
  python manage.py makemigrations tenants buildings users announcements votes user_requests
"

# Step 2: Recreate Public Schema and Shared Migrations
echo ""
echo "🛠️ Recreating public schema and applying shared migrations..."
docker compose exec -T web bash -c "
  python manage.py migrate_schemas --shared
"

# Step 3: Execute Reset + Create Tenant Script
echo ""
echo "✨ Running reset_and_create_tenant.py script..."
docker compose exec -T web bash -c "
  python manage.py shell < scripts/reset_and_create_tenant.py
"

echo ""
echo "✅ RESET COMPLETE!"
echo ""
