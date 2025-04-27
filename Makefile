# Makefile για Digital Concierge

.PHONY: help migrate createsuperuser shell reset runserver

help:
	@echo "Διαθέσιμες εντολές:"
	@echo "  make migrate           --> Κάνει migrate schemas (shared)"
	@echo "  make createsuperuser   --> Δημιουργεί Django superuser"
	@echo "  make shell             --> Μπαίνει σε Django shell"
	@echo "  make reset             --> Κάνει full reset και δημιουργεί tenant"
	@echo "  make runserver         --> Τρέχει τον development server"

migrate:
	docker compose exec web python manage.py migrate_schemas --shared

createsuperuser:
	docker compose exec web python manage.py createsuperuser

shell:
	docker compose exec web python manage.py shell

reset:
	docker compose exec web python manage.py shell < scripts/reset_and_create_tenant.py

runserver:
	docker compose exec web python manage.py runserver 0.0.0.0:8000
