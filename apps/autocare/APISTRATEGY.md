REFERENCE TABLES
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Year --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Make --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Model --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/SubModel --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Region --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleTypeGroup --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Class --pagesize 1000

ATTRIBUTE TABLES
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/DriveType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/FuelType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/TransmissionType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/TransmissionControlType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/TransmissionNumSpeeds --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/SteeringType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/SteeringSystem --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BrakeType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BrakeSystem --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BrakeABS --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/SpringType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Valves --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Aspiration --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/CylinderHeadType --pagesize 1000

CONFIGURATION TABLES
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/EngineBlock --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/EngineBoreStroke --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/EngineBase --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/EngineConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/TransmissionBase --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BrakeConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/SteeringConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/SpringTypeConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BodyStyleConfig --pagesize 1000

CORE VEHICLES (HIGH VOLUME)
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BaseVehicle --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Vehicle --pagesize 1000

FITMENT TABLES (VERY LARGE)
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleToEngineConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleToTransmission --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleToBodyConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleToDriveType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleToBedConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleToWheelBase --pagesize 1000

Skip /vcdb/equipment and /vcdb/VCdbChanges

docker compose exec db pg_dump -U postgres -Fc -t autocare_autocarerawrecord nexus > data/autocare/raw/vcdb_raw_$(date +%F).dump

# 1. Fetch Swagger
docker compose exec web python manage.py fetch_autocare_swagger

# 2. Reconcile against raw data
docker compose exec web python manage.py reconcile_autocare_schema

# 3. Snapshot schema
docker compose exec web python manage.py snapshot_autocare_schema

# 4. Detect drift
docker compose exec web python manage.py detect_autocare_schema_drift

# 5. Generate models for review
docker compose exec web python manage.py generate_autocare_models --fk-mode safe
