#!/bin/bash

echo "🔧 Updating settings to move 'buildings' to SHARED_APPS..."

# 1. Επεξεργασία αρχείου settings.py (χειροκίνητα ή με VS Code)

echo "✅ Please ensure in config/settings.py you have:"
echo ""
echo "SHARED_APPS = ["
echo "    ...,"
echo "    'buildings',"
echo "]"
echo ""
echo "TENANT_APPS = ["
echo "    ... (ΧΩΡΙΣ το 'buildings')"
echo "]"
echo ""
read -p "📌 Press Enter to confirm and continue..."

# 2. Δημιουργία migration
echo "📦 Running makemigrations for buildings..."
docker-compose exec web python manage.py makemigrations buildings

# 3. Εκτέλεση στο public schema
echo "⚙️  Running migrate_schemas --shared..."
docker-compose exec web python manage.py migrate_schemas --shared

echo ""
echo "✅ Done! The buildings tables now exist in the public schema."
