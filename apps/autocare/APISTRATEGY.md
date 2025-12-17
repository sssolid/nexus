REFERENCE TABLES
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Year --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Make --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Model --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/SubModel --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Region --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleTypeGroup --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Class --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Abbreviation --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/PublicationStage --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Mfr --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/MfrBodyCode --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BodyType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BodyNumDoors --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BedType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BedLength --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/WheelBase --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/Transmission --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/TransmissionMfrCode --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/ElecControlled --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/PowerOutput --pagesize 1000

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
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/EngineDesignation --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/EngineVersion --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/EngineVin --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/EngineConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/TransmissionBase --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BrakeConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/SteeringConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/SpringTypeConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BodyStyleConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/BedConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/FuelDeliveryConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/FuelDeliveryType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/FuelDeliverySubType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/FuelSystemControlType --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/FuelSystemDesign --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/IgnitionSystemType --pagesize 1000

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
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleToClass --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleToBrakeConfig --pagesize 1000
docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleToBodyStyleConfig --pagesize 1000
- docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleToSpringTypeConfig --pagesize 1000
- (NEED TO RESUME) docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleToSteeringConfig --pagesize 1000
docker compose exec web python manage.py ingest_autocare --db vcdb /vcdb/VehicleToMfrBodyCode --pagesize 1000

Skip /vcdb/equipment and /vcdb/VCdbChanges

# Create a raw dump of the raw data
docker compose exec db pg_dump -U postgres -Fc -t autocare_autocarerawrecord nexus > data/autocare/raw/vcdb_raw_$(date +%F).dump
# IF YOU NEED TO IMPORT THIS DUMP
cat data/autocare/raw/vcdb_raw_2025-12-15.dump | \
docker compose exec -T db pg_restore \
  -U postgres \
  -d nexus \
  --clean \
  --if-exists


# Create the staging database to generate django models from
# MAKE SURE THE SCHEMA FROM AUTOCARE HAS QUOTES AROUND THE TABLE NAMES AND FIELDS (IT DOESN'T ON ALL OF THEM)
docker compose exec web psql -h db -U postgres -d nexus -v ON_ERROR_STOP=1 -c "DROP SCHEMA IF EXISTS staging CASCADE; CREATE SCHEMA staging;"
docker compose exec web psql -h db -U postgres -d nexus -v ON_ERROR_STOP=1 -c "SET search_path TO staging;" -f /app/src/data/autocare/db_schema/vcdb_schema.sql

# Generate the django models
# Before doing so check the models as there are some manual changes that need to be done
# For example:
# v_cdb_changes.py should be vcdb_changes.py
#   the id field should be vcdb_change_id = models.IntegerField(db_column='ID')
# vehicle_to_class.py:
# class_ should be...
# vehicle_class = models.ForeignKey('VehicleClass', db_column='ClassID', db_index=True, on_delete=models.DO_NOTHING)
# THE FUCKING CODE IS NOT DOING CamelCase PROPERLY AND NEEDS TO BE FIXED IMMEDIATELY
docker compose exec web python manage.py generate_autocare_models

# Verify the models
docker compose exec web python manage.py validate_autocare_models

# Generate the migrations
docker compose exec web python manage.py makemigrations autocare

# Migrate the data
docker compose exec web python manage.py migrate autocare