import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_tenants.utils import schema_context
from buildings.models import Building
from users.models import UserProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Bulk add users to a specific building within a tenant schema from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--schema', type=str, required=True, help='Schema name (tenant)')
        parser.add_argument('--building', type=str, required=True, help='Building code')
        parser.add_argument('--file', type=str, required=True, help='Path to CSV file')

    def handle(self, *args, **options):
        schema = options['schema']
        building_code = options['building']
        file_path = options['file']

        try:
            with schema_context(schema):
                try:
                    building = Building.objects.get(code=building_code)
                except Building.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Building with code '{building_code}' not found in schema '{schema}'"))
                    return

                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    count = 0
                    for row in reader:
                        username = row['username']
                        email = row['email']
                        password = row['password']
                        role = row['role']
                        phone = row.get('phone', '')

                        if User.objects.filter(username=username).exists():
                            self.stdout.write(self.style.WARNING(f"User '{username}' already exists. Skipping."))
                            continue

                        user = User.objects.create_user(username=username, email=email, password=password)
                        # Ensure profile exists (if using signals, this may not be needed)
                        profile, _ = UserProfile.objects.get_or_create(user=user)
                        profile.role = role
                        profile.phone = phone
                        profile.building = building
                        profile.save()
                        count += 1

                self.stdout.write(self.style.SUCCESS(f"Successfully added {count} users to building '{building.name}' (schema: {schema})"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))