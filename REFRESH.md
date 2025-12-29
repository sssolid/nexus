docker compose exec web bash -c '                                                                                                                                                                                                                                                                     130 ↵
set -e
export PGPASSWORD=postgres

psql -h db -U postgres -d nexus -v ON_ERROR_STOP=1 -c "DROP SCHEMA IF EXISTS staging_vcdb CASCADE; CREATE SCHEMA staging_vcdb;"
psql -h db -U postgres -d nexus -v ON_ERROR_STOP=1 -c "SET search_path TO staging_vcdb;" -f /app/src/data/autocare/db_schema/vcdb_schema.sql
python manage.py generate_autocare_models --schema staging_vcdb --output-dir apps/autocare/models/_staging_dump/vcdb

psql -h db -U postgres -d nexus -v ON_ERROR_STOP=1 -c "DROP SCHEMA IF EXISTS staging_pcdb CASCADE; CREATE SCHEMA staging_pcdb;"
psql -h db -U postgres -d nexus -v ON_ERROR_STOP=1 -c "SET search_path TO staging_pcdb;" -f /app/src/data/autocare/db_schema/pcdb_schema.sql
python manage.py generate_autocare_models --schema staging_pcdb --output-dir apps/autocare/models/_staging_dump/pcdb

psql -h db -U postgres -d nexus -v ON_ERROR_STOP=1 -c "DROP SCHEMA IF EXISTS staging_padb CASCADE; CREATE SCHEMA staging_padb;"
psql -h db -U postgres -d nexus -v ON_ERROR_STOP=1 -c "SET search_path TO staging_padb;" -f /app/src/data/autocare/db_schema/padb_schema.sql
python manage.py generate_autocare_models --schema staging_padb --output-dir apps/autocare/models/_staging_dump/padb

psql -h db -U postgres -d nexus -v ON_ERROR_STOP=1 -c "DROP SCHEMA IF EXISTS staging_qdb CASCADE; CREATE SCHEMA staging_qdb;"
psql -h db -U postgres -d nexus -v ON_ERROR_STOP=1 -c "SET search_path TO staging_qdb;"  -f /app/src/data/autocare/db_schema/qdb_schema.sql
python manage.py generate_autocare_models --schema staging_qdb  --output-dir apps/autocare/models/_staging_dump/qdb
'

docker compose exec db psql -U postgres -d nexus -c "
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
"

find apps/autocare -path "*/migrations/*.py" -not -name "__init__.py" -delete
find apps/autocare -path "*/migrations/*.pyc" -delete

docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

docker compose exec -T db psql -U postgres -d nexus < data/autocare/raw/rawrecord_data.sql

docker compose exec web python manage.py ingest_payloads  \
  --db vcdb \
  --asof 2025-12-18 \
  --app-label autocare_vcdb
  --order auto_fk \
  --skip-missing-vehicles \
  --skip-missing-engineconfig2

docker compose exec web python manage.py ingest_payloads \
  --db pcdb \
  --asof 2025-12-18 \
  --app-label autocare_pcdb

docker compose exec web python manage.py ingest_payloads \
  --db padb \
  --asof 2025-12-18 \
  --app-label autocare_padb

docker compose exec web python manage.py ingest_aces data/autocare/aces/WORKING_PH_BKMN_ACES42_20250826153314_79564da30eda.xml


NUKE THE AUTOCARE DATABASES
```
DROP SCHEMA IF EXISTS autocare_vcdb CASCADE;
DROP SCHEMA IF EXISTS autocare_pcdb CASCADE;
DROP SCHEMA IF EXISTS autocare_padb CASCADE;
DROP SCHEMA IF EXISTS autocare_qdb CASCADE;
DROP SCHEMA IF EXISTS autocare_brand CASCADE;

DELETE FROM django_migrations WHERE app LIKE 'autocare_%';

CREATE SCHEMA autocare_vcdb;
CREATE SCHEMA autocare_pcdb;
CREATE SCHEMA autocare_padb;
CREATE SCHEMA autocare_qdb;
CREATE SCHEMA autocare_brand;

docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```