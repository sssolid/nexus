# Autocare Full Rebuild Runbook

**Audience:** Infrastructure / Data Engineering  
**Use when:** Autocare schemas are corrupted, ingestion logic breaks, or a clean baseline is required.

---

## 1. Regenerate ACES & PIES Schemas

```bash
xsdata generate data/autocare/documentation/pies/PIES_7_2_Documentation/PIES_7_2_XSDSchema_Rev4_2_27_2025.xsd \
  --package apps.autocare.pies.schemas \
  --output dataclasses \
  --config data/xsdata.xml

xsdata generate data/autocare/documentation/aces/ACES_4_2_Documentation/ACES_4_2_XSDSchema_Rev2_11_19_2021.xsd \
  --package apps.autocare.aces.schemas \
  --output dataclasses \
  --config data/xsdata.xml
```

---

## 2. Rebuild Vendor Staging Schemas (VCDB / PCDB / PADB / QDB)

```bash
docker compose exec web bash -c '
set -e
export PGPASSWORD=postgres
DB="psql -h db -U postgres -d nexus -v ON_ERROR_STOP=1"

$DB -c "DROP SCHEMA IF EXISTS staging_vcdb CASCADE; CREATE SCHEMA staging_vcdb;"
$DB -c "SET search_path TO staging_vcdb;" -f /app/src/data/autocare/db_schema/vcdb_schema.sql
python manage.py generate_autocare_models --schema staging_vcdb --output-dir apps/autocare/models/_staging_dump/vcdb

$DB -c "DROP SCHEMA IF EXISTS staging_pcdb CASCADE; CREATE SCHEMA staging_pcdb;"
$DB -c "SET search_path TO staging_pcdb;" -f /app/src/data/autocare/db_schema/pcdb_schema.sql
python manage.py generate_autocare_models --schema staging_pcdb --output-dir apps/autocare/models/_staging_dump/pcdb

$DB -c "DROP SCHEMA IF EXISTS staging_padb CASCADE; CREATE SCHEMA staging_padb;"
$DB -c "SET search_path TO staging_padb;" -f /app/src/data/autocare/db_schema/padb_schema.sql
python manage.py generate_autocare_models --schema staging_padb --output-dir apps/autocare/models/_staging_dump/padb

$DB -c "DROP SCHEMA IF EXISTS staging_qdb CASCADE; CREATE SCHEMA staging_qdb;"
$DB -c "SET search_path TO staging_qdb;" -f /app/src/data/autocare/db_schema/qdb_schema.sql
python manage.py generate_autocare_models --schema staging_qdb --output-dir apps/autocare/models/_staging_dump/qdb
'
```

---

## 3. Reset Django Schema State

```bash
docker compose exec db psql -U postgres -d nexus -c "
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
"
```

---

## 4. Delete All Autocare Migrations

```bash
find apps/autocare -path "*/migrations/*.py" -not -name "__init__.py" -delete
find apps/autocare -path "*/migrations/*.pyc" -delete
```

---

## 5. Rebuild Django Models

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

---

## 6. Load Raw Record Seed Data

```bash
docker compose exec -T db psql -U postgres -d nexus < data/autocare/raw/rawrecord_data.sql
```

---

## 7. Baseline VCDB / PCDB / PADB Ingest

```bash
docker compose exec web python manage.py ingest_payloads \
  --db vcdb \
  --asof 2025-12-18 \
  --app-label autocare_vcdb \
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
```

---

## 8. Import ACES XML

```bash
docker compose exec web python manage.py ingest_aces \
  data/autocare/aces/WORKING_PH_BKMN_ACES42_20250826153314_79564da30eda.xml
```

---

## 9. Emergency Nuke – Autocare Schemas Only

Use when corruption cannot be recovered.

```sql
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
```

Then rerun:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

## 10. FileMaker Data Dictionary Export (Mapping Review)

**Purpose:**
Snapshot FileMaker field definitions so you can verify which fields must be mapped into your Django sync layer.

```python
from services.filemaker_client import FileMakerClient
from django.conf import settings
import json

fm = FileMakerClient(password=settings.FILEMAKER_PASSWORD)

dictionary = fm.export_data_dictionary(["Master"])

with open("filemaker_data_dictionary.json", "w") as f:
    json.dump(dictionary, f, indent=2)
```

**Output:**
`filemaker_data_dictionary.json` – canonical reference for mapping decisions.

---

## 11. Bring Development Containers Down / Up

**Use when rebuilding environments or after schema nukes.**

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

---

## 12. ACES XML Ingest

```bash
docker compose exec web python manage.py ingest_aces \
  data/autocare/aces/WORKING_PH_BKMN_ACES42_20250826153314_79564da30eda.xml
```

---

## 13. PIES XML Ingest (placeholder)

Once the PIES parser is finalized, this becomes:

```bash
docker compose exec web python manage.py ingest_pies \
  data/autocare/pies/<PIES_XML_FILENAME>.xml
```