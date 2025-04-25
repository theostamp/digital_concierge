cd C:\Users\thodo\digital_concierge\frontend    

npm run dev


cd C:\Users\thodo\digital_concierge
.\setup-vscode-settings.ps1
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass


.\venv\Scripts\activate
python manage.py exporttree --output dev_tree.md

python manage.py makemigrations
python manage.py makemigrations users
python manage.py makemigrations announcements
python manage.py makemigrations votes
python manage.py makemigrations tenants

python manage.py migrate
python manage.py migrate_schemas
python manage.py migrate --fake-initial --run-syncdb --database=default
python manage.py migrate_schemas --shared	
python manage.py migrate_schemas --tenant	
python manage.py migrate_schemas --schema=etairia1	

bash scripts/setup_shared.sh


echo "# digital_concierge" >> README.md
git init

git add .
git commit -m "1"
git branch -M main
git remote add origin https://github.com/theostamp/digital_concierge.git
git push -u origin main

git push --force

cd frontend

npm run build
npm run dev








# Διακοπή και διαγραφή όλων των containers
.\docker_cleanup.ps1


# Διακοπή και διαγραφή όλων των containers
docker-compose down --volumes --remove-orphans

# Εάν έχεις standalone containers που δεν είναι μέρος του docker-compose
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

# Διαγραφή volumes που δεν χρησιμοποιούνται
docker volume prune -f

# Διαγραφή δικτύων που δημιουργήθηκαν από το Docker Compose
docker network prune -f
docker system prune -a --volumes

docker volume rm $(docker volume ls -q)
docker network rm $(docker network ls -q)


docker-compose down
docker-compose up --build

docker exec -it odoo18 /bin/bash
odoo shell -d oiko
env['ir.ui.menu'].search([('name', 'ilike', 'POS')])
env['ir.model.data'].search([('model', '=', 'ir.ui.menu'), ('name', 'ilike', 'point_of_sale')]).read(['name', 'model', 'res_id'])

env['restaurant.table']._fields

bash delete_pycache.sh
sudo chmod -R 755 /mnt/c/Users/Notebook/odoo_docker

chmod -R 777 /

./odoo-bin -u pos_restaurant -d oiko

docker exec -it odoo_docker-odoo-1 /bin/bash

docker exec -u root -it odoo_docker-odoo-1  /bin/bash

./odoo-bin -c odoo.conf -d  oiko -u all --dev=all

docker exec -it odoo18 bash

find /usr/lib/python3/dist-packages/ -name "__pycache__" -type d -exec rm -rf {} + && echo "Cache cleared successfully"

<!-- Εκτέλεσε μια επανεγκατάσταση του module με την ακόλουθη εντολή: -->

odoo -c /etc/odoo/odoo.conf -d  oiko -u Restaurant

docker system prune -a --volumes

sudo find . -name "__pycache__" -type d -exec rm -rf {} +

echo "# odoo" >> README.md
git init

git add .
git commit -m "Ok all"
git branch -M main
git remote add origin https://github.com/theostamp/gpt_odoo.git
git push -u origin main

git push -u origin main --force

Διαγραφή Cache του Odoo

--------------------------------------------------------

docker exec -it odoo18 bash
service odoo stop
rm -rf /var/lib/odoo/.local/share/Odoo/sessions/*
rm -rf /var/lib/odoo/.local/share/Odoo/cache/*
rm -rf /var/lib/odoo/.local/share/Odoo/assets/*
find /mnt/custom-addons -type f -name "*.pyc" -delete
find /mnt/custom-addons -type f -name "*.pyo" -delete
find /mnt/custom-addons -type d -name "__pycache__" -exec rm -r {} +
sudo chown -R odoo:odoo /var/lib/odoo/.local
sudo chown -R odoo:odoo /mnt/custom-addons
sudoo service odoo start
tail -f /var/log/odoo/odoo-server.log
service odoo restart

---------------------------------------------------------

sudo chown -R odoo:odoo /var/lib/odoo/.local/share/Odoo/filestore/
./odoo --db-filter=<your_database> -c odoo.conf -u all

exit

docker-compose down
docker-compose up -d --build

odoo -u all --db  oiko

systemctl status odoo

grep -r "FloorScreen" /usr/lib/python3/dist-packages/odoo/addons/pos_restaurant

grep -r "t-name="pos_restaurant.FloorScreen"" /usr/lib/python3/dist-packages/odoo/addons/pos_restaurant

grep -r "t-name" /usr/lib/python3/dist-packages/odoo/addons/pos_restaurant

grep -r "floor-map" /usr/lib/python3/dist-packages/odoo/addons/pos_restaurant

class="floor-map"

grep -r "floor_screen.js" /usr/lib/python3/dist-packages/odoo/addons/

id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_restaurant_floor,restaurant.floor.user,model_restaurant_floor,point_of_sale.group_pos_user,1,0,0,0
access_restaurant_floor_manager,restaurant.floor.manager,model_restaurant_floor,point_of_sale.group_pos_manager,1,1,1,1
access_restaurant_table,restaurant.table.user,model_restaurant_table,point_of_sale.group_pos_user,1,0,0,0
access_restaurant_table_manager,restaurant.table.manager,model_restaurant_table,point_of_sale.group_pos_manager,1,1,1,1

odoo shell -d sa

python3 /mnt/custom-addons/scan.py

sudo chown -R odoo:odoo /mnt/custom-addons
chmod -R 755 /mnt/custom-addons

sudo chmod -R 755 /mnt/custom-addons

docker exec -it -u root odoo18 /bin/bash
docker exec -it odoo18 bash

sudo chmod -R 755 /mnt/custom-addons/pos_time

Καθαρισμός των assets:

rm -rf /var/lib/odoo/filestore/*/assets*
rm -rf ~/.cache/odoo/*

Επανεκκίνηση και ενημέρωση του module:

/usr/bin/odoo -c /etc/odoo/odoo.conf -d oiko -u pos_time

docker exec -it odoo18 /bin/bash
odoo shell -d oiko

# Στο Odoo shell:

products = env['product.template'].search([('is_kitchen_product', '=', True)])
print(f"Kitchen products: {len(products)}")

orders = env['kitchen.order'].search([])
print(f"Kitchen orders: {len(orders)}")

pos_orders = env['pos.order'].search([])
print(f"POS orders: {len(pos_orders)}")

# Διακοπή και διαγραφή όλων των containers

docker-compose down --volumes --remove-orphans

# Εάν έχεις standalone containers που δεν είναι μέρος του docker-compose

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

# Διαγραφή volumes που δεν χρησιμοποιούνται

docker volume prune -f

# Διαγραφή δικτύων που δημιουργήθηκαν από το Docker Compose

docker network prune -f

docker image prune -a
docker image prune -a -f
docker system prune -a --volumes

docker rm $(docker ps -aq)
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -q)
docker network rm $(docker network ls -q)
docker system prune -a

docker-compose down
docker-compose up --build

docker exec -it odoo18 /bin/bash
odoo shell -d oiko
env['ir.ui.menu'].search([('name', 'ilike', 'POS')])
env['ir.model.data'].search([('model', '=', 'ir.ui.menu'), ('name', 'ilike', 'point_of_sale')]).read(['name', 'model', 'res_id'])

env['restaurant.table']._fields

bash delete_pycache.sh
sudo chmod -R 755 /mnt/c/Users/Notebook/odoo_docker

chmod -R 777 /

./odoo-bin -u pos_restaurant -d oiko

docker exec -it odoo_docker-odoo-1 /bin/bash

docker exec -u root -it odoo_docker-odoo-1  /bin/bash

./odoo-bin -c odoo.conf -d  oiko -u all --dev=all

docker exec -it odoo18 bash

find /usr/lib/python3/dist-packages/ -name "__pycache__" -type d -exec rm -rf {} + && echo "Cache cleared successfully"

<!-- Εκτέλεσε μια επανεγκατάσταση του module με την ακόλουθη εντολή: -->

odoo -c /etc/odoo/odoo.conf -d  oiko -u Restaurant

docker system prune -a --volumes

sudo find . -name "__pycache__" -type d -exec rm -rf {} +

echo "# odoo" >> README.md
git init

git add .
git commit -m "Ok all"
git branch -M main
git remote add origin https://github.com/theostamp/gpt_odoo.git
git push -u origin main

git push -u origin main --force

Διαγραφή Cache του Odoo

---

docker exec -it odoo18 bash

# Stop Odoo service

service odoo stop

# Clear Odoo cache and sessions

rm -rf /var/lib/odoo/.local/share/Odoo/sessions/*
rm -rf /var/lib/odoo/.local/share/Odoo/cache/*
rm -rf /var/lib/odoo/.local/share/Odoo/assets/*

# Clear Python cache files

find /mnt/custom-addons -type f -name "*.pyc" -delete
find /mnt/custom-addons -type f -name "*.pyo" -delete
find /mnt/custom-addons -type d -name "__pycache__" -exec rm -r {} +

# Reset permissions

sudo chown -R odoo:odoo /var/lib/odoo/.local
sudo chown -R odoo:odoo /mnt/custom-addons

# Start Odoo service

sudoo service odoo start

# Optional: Check logs for errors

tail -f /var/log/odoo/odoo-server.log
service odoo restart

---

sudo chown -R odoo:odoo /var/lib/odoo/.local/share/Odoo/filestore/
./odoo --db-filter=<your_database> -c odoo.conf -u all

exit

docker-compose down
docker-compose up -d --build

odoo -u all --db  oiko

systemctl status odoo

grep -r "FloorScreen" /usr/lib/python3/dist-packages/odoo/addons/pos_restaurant

grep -r "t-name="pos_restaurant.FloorScreen"" /usr/lib/python3/dist-packages/odoo/addons/pos_restaurant

grep -r "t-name" /usr/lib/python3/dist-packages/odoo/addons/pos_restaurant

grep -r "floor-map" /usr/lib/python3/dist-packages/odoo/addons/pos_restaurant

class="floor-map"

grep -r "floor_screen.js" /usr/lib/python3/dist-packages/odoo/addons/

id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_restaurant_floor,restaurant.floor.user,model_restaurant_floor,point_of_sale.group_pos_user,1,0,0,0
access_restaurant_floor_manager,restaurant.floor.manager,model_restaurant_floor,point_of_sale.group_pos_manager,1,1,1,1
access_restaurant_table,restaurant.table.user,model_restaurant_table,point_of_sale.group_pos_user,1,0,0,0
access_restaurant_table_manager,restaurant.table.manager,model_restaurant_table,point_of_sale.group_pos_manager,1,1,1,1

odoo shell -d sa

python3 /mnt/custom-addons/scan.py

sudo chown -R odoo:odoo /mnt/custom-addons
chmod -R 755 /mnt/custom-addons

sudo chmod -R 755 /mnt/custom-addons

docker exec -it -u root odoo18 /bin/bash
docker exec -it odoo18 bash

sudo chmod -R 755 /mnt/custom-addons/pos_time

Καθαρισμός των assets:

rm -rf /var/lib/odoo/filestore/*/assets*
rm -rf ~/.cache/odoo/*

Επανεκκίνηση και ενημέρωση του module:

/usr/bin/odoo -c /etc/odoo/odoo.conf -d oiko -u pos_time

docker exec -it odoo18 /bin/bash
odoo shell -d oiko

# Στο Odoo shell:

products = env['product.template'].search([('is_kitchen_product', '=', True)])
print(f"Kitchen products: {len(products)}")

orders = env['kitchen.order'].search([])
print(f"Kitchen orders: {len(orders)}")

pos_orders = env['pos.order'].search([])
print(f"POS orders: {len(pos_orders)}")

docker-compose down --volumes --remove-orphans

# Εάν έχεις standalone containers που δεν είναι μέρος του docker-compose

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

# Διαγραφή volumes που δεν χρησιμοποιούνται

docker volume prune -f

# Διαγραφή δικτύων που δημιουργήθηκαν από το Docker Compose

docker network prune -f

docker image prune -a
docker image prune -a -f
docker system prune -a --volumes

docker rm $(docker ps -aq)
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -q)
docker network rm $(docker network ls -q)
docker system prune -a

docker-compose down
docker-compose up --build

docker exec -it odoo18 /bin/bash
odoo shell -d oiko
env['ir.ui.menu'].search([('name', 'ilike', 'POS')])
env['ir.model.data'].search([('model', '=', 'ir.ui.menu'), ('name', 'ilike', 'point_of_sale')]).read(['name', 'model', 'res_id'])

env['restaurant.table']._fields

bash delete_pycache.sh
sudo chmod -R 755 /mnt/c/Users/Notebook/odoo_docker

chmod -R 777 /

./odoo-bin -u pos_restaurant -d oiko

docker exec -it odoo_docker-odoo-1 /bin/bash

docker exec -u root -it odoo_docker-odoo-1  /bin/bash

./odoo-bin -c odoo.conf -d  oiko -u all --dev=all

docker exec -it odoo18 bash

find /usr/lib/python3/dist-packages/ -name "__pycache__" -type d -exec rm -rf {} + && echo "Cache cleared successfully"

<!-- Εκτέλεσε μια επανεγκατάσταση του module με την ακόλουθη εντολή: -->

odoo -c /etc/odoo/odoo.conf -d  oiko -u Restaurant

docker system prune -a --volumes

sudo find . -name "__pycache__" -type d -exec rm -rf {} +

echo "# odoo" >> README.md
git init

git add .
git commit -m "Ok all"
git branch -M main
git remote add origin https://github.com/theostamp/gpt_odoo.git
git push -u origin main

git push -u origin main --force

Διαγραφή Cache του Odoo

---

docker exec -it odoo18 bash

# Stop Odoo service

service odoo stop

# Clear Odoo cache and sessions

rm -rf /var/lib/odoo/.local/share/Odoo/sessions/*
rm -rf /var/lib/odoo/.local/share/Odoo/cache/*
rm -rf /var/lib/odoo/.local/share/Odoo/assets/*

# Clear Python cache files

find /mnt/custom-addons -type f -name "*.pyc" -delete
find /mnt/custom-addons -type f -name "*.pyo" -delete
find /mnt/custom-addons -type d -name "__pycache__" -exec rm -r {} +

# Reset permissions

sudo chown -R odoo:odoo /var/lib/odoo/.local
sudo chown -R odoo:odoo /mnt/custom-addons

# Start Odoo service

sudoo service odoo start

# Optional: Check logs for errors

tail -f /var/log/odoo/odoo-server.log
service odoo restart

---

sudo chown -R odoo:odoo /var/lib/odoo/.local/share/Odoo/filestore/
./odoo --db-filter=<your_database> -c odoo.conf -u all

exit

docker-compose down
docker-compose up -d --build

odoo -u all --db  oiko

systemctl status odoo

grep -r "FloorScreen" /usr/lib/python3/dist-packages/odoo/addons/pos_restaurant

grep -r "t-name="pos_restaurant.FloorScreen"" /usr/lib/python3/dist-packages/odoo/addons/pos_restaurant

grep -r "t-name" /usr/lib/python3/dist-packages/odoo/addons/pos_restaurant

grep -r "floor-map" /usr/lib/python3/dist-packages/odoo/addons/pos_restaurant

class="floor-map"

grep -r "floor_screen.js" /usr/lib/python3/dist-packages/odoo/addons/

id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_restaurant_floor,restaurant.floor.user,model_restaurant_floor,point_of_sale.group_pos_user,1,0,0,0
access_restaurant_floor_manager,restaurant.floor.manager,model_restaurant_floor,point_of_sale.group_pos_manager,1,1,1,1
access_restaurant_table,restaurant.table.user,model_restaurant_table,point_of_sale.group_pos_user,1,0,0,0
access_restaurant_table_manager,restaurant.table.manager,model_restaurant_table,point_of_sale.group_pos_manager,1,1,1,1

odoo shell -d sa

python3 /mnt/custom-addons/scan.py

sudo chown -R odoo:odoo /mnt/custom-addons
chmod -R 755 /mnt/custom-addons

sudo chmod -R 755 /mnt/custom-addons

docker exec -it -u root odoo18 /bin/bash
docker exec -it odoo18 bash

sudo chmod -R 755 /mnt/custom-addons/pos_time

Καθαρισμός των assets:

rm -rf /var/lib/odoo/filestore/*/assets*
rm -rf ~/.cache/odoo/*

Επανεκκίνηση και ενημέρωση του module:

/usr/bin/odoo -c /etc/odoo/odoo.conf -d oiko -u pos_time

docker exec -it odoo18 /bin/bash
odoo shell -d oiko

# Στο Odoo shell:

products = env['product.template'].search([('is_kitchen_product', '=', True)])
print(f"Kitchen products: {len(products)}")

orders = env['kitchen.order'].search([])
print(f"Kitchen orders: {len(orders)}")

pos_orders = env['pos.order'].search([])
print(f"POS orders: {len(pos_orders)}")
