-- Initialize PostgreSQL database with optimizations for Django application

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For trigram text search
CREATE EXTENSION IF NOT EXISTS "btree_gin"; -- For composite indexes

-- Full text search configuration
ALTER DATABASE nexus SET default_text_search_config = 'pg_catalog.english';

-- ================================================================
-- AutoCare Schema Initialization for Development
-- ================================================================

-- Create main schemas
CREATE SCHEMA IF NOT EXISTS autocare_vcdb;
CREATE SCHEMA IF NOT EXISTS autocare_pcdb;
CREATE SCHEMA IF NOT EXISTS autocare_padb;
CREATE SCHEMA IF NOT EXISTS autocare_qdb;
CREATE SCHEMA IF NOT EXISTS autocare_brand;
CREATE SCHEMA IF NOT EXISTS autocare_reference;
CREATE SCHEMA IF NOT EXISTS autocare_aces_raw;
CREATE SCHEMA IF NOT EXISTS autocare_pies_raw;
CREATE SCHEMA IF NOT EXISTS autocare_aces;
CREATE SCHEMA IF NOT EXISTS autocare_pies;
CREATE SCHEMA IF NOT EXISTS autocare_shared;

-- Optional Crown schema if you want to separate your own models
CREATE SCHEMA IF NOT EXISTS crown;

-- Grant permissions for your Django user
GRANT USAGE ON SCHEMA autocare_vcdb TO postgres;
GRANT USAGE ON SCHEMA autocare_pcdb TO postgres;
GRANT USAGE ON SCHEMA autocare_padb TO postgres;
GRANT USAGE ON SCHEMA autocare_qdb TO postgres;
GRANT USAGE ON SCHEMA autocare_brand TO postgres;
GRANT USAGE ON SCHEMA autocare_reference TO postgres;
GRANT USAGE ON SCHEMA autocare_aces_raw TO postgres;
GRANT USAGE ON SCHEMA autocare_pies_raw TO postgres;
GRANT USAGE ON SCHEMA autocare_aces TO postgres;
GRANT USAGE ON SCHEMA autocare_pies TO postgres;
GRANT USAGE ON SCHEMA autocare_shared TO postgres;

GRANT SELECT ON ALL TABLES IN SCHEMA autocare_vcdb TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_pcdb TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_padb TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_qdb TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_brand TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_reference TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_aces_raw TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_pies_raw TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_aces TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_pies TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_shared TO postgres;

-- Ensure new tables created manually inherit permissions
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_vcdb GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_pcdb GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_padb GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_qdb GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_brand GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_reference GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_aces_raw GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_pies_raw GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_aces GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_pies GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_shared GRANT SELECT ON TABLES TO postgres;

-- Crown-specific permissions (optional)
GRANT ALL PRIVILEGES ON SCHEMA crown TO postgres;

-- ACES & PIES raw data table
CREATE TABLE autocare_aces_raw.app (
    id BIGSERIAL PRIMARY KEY,
    source_file TEXT NOT NULL,
    app_id INTEGER,
    action CHAR(1),
    validate BOOLEAN DEFAULT TRUE,
    part_number TEXT,
    part_type_id INTEGER,
    quantity INTEGER,
    position_id INTEGER,
    brand_aaiaid TEXT,
    subbrand_aaiaid TEXT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE autocare_aces_raw.app_vehicle (
    id BIGSERIAL PRIMARY KEY,
    app_id INTEGER,
    base_vehicle_id INTEGER,
    make_id INTEGER,
    model_id INTEGER,
    submodel_id INTEGER,
    year_from INTEGER,
    year_to INTEGER,
    engine_base_id INTEGER,
    engine_block_id INTEGER,
    engine_vin_id INTEGER,
    aspiration_id INTEGER,
    equipment_model_id INTEGER,
    equipment_base_id INTEGER,
    vehicle_type_id INTEGER,
    production_start INTEGER,
    production_end INTEGER
);

CREATE TABLE autocare_aces_raw.app_qualifier (
    id BIGSERIAL PRIMARY KEY,
    app_id INTEGER,
    qual_id INTEGER,
    qual_text TEXT,
    param_1 TEXT,
    param_2 TEXT,
    param_3 TEXT
);

CREATE TABLE autocare_aces_raw.asset (
    id BIGSERIAL PRIMARY KEY,
    asset_name TEXT,
    make_id INTEGER,
    model_id INTEGER,
    submodel_id INTEGER,
    engine_base_id INTEGER,
    year_from INTEGER,
    year_to INTEGER,
    note TEXT
);

CREATE TABLE autocare_aces_raw.digital_asset (
    id BIGSERIAL PRIMARY KEY,
    asset_name TEXT,
    file_name TEXT,
    uri TEXT,
    file_type TEXT,
    file_size INTEGER,
    width INTEGER,
    height INTEGER,
    effective_date DATE,
    expiration_date DATE
);

CREATE TABLE IF NOT EXISTS autocare_aces_raw.app_attribute (
    id BIGSERIAL PRIMARY KEY,
    source_file TEXT NOT NULL,
    app_id INTEGER NOT NULL,
    attr_name TEXT NOT NULL,              -- e.g. 'mfr_body_code'
    attr_id INTEGER NULL,                 -- e.g. 242
    attr_value TEXT NULL,                 -- for rare non-id values
    idx SMALLINT NOT NULL DEFAULT 0        -- for list fields like sub_model[0..1]
);

CREATE INDEX IF NOT EXISTS app_attribute_app_id_idx
    ON autocare_aces_raw.app_attribute(app_id);

CREATE INDEX IF NOT EXISTS app_attribute_name_id_idx
    ON autocare_aces_raw.app_attribute(attr_name, attr_id);

-- TODO: ADD THESE
-- ALTER TABLE autocare_aces_raw.app_vehicle
--   ADD COLUMN IF NOT EXISTS submodel_id              integer,
--   ADD COLUMN IF NOT EXISTS mfr_id                   integer,
--   ADD COLUMN IF NOT EXISTS mfr_body_code_id         integer,
--   ADD COLUMN IF NOT EXISTS transmission_control_type_id integer,
--   ADD COLUMN IF NOT EXISTS transmission_base_id     integer,
--   ADD COLUMN IF NOT EXISTS transmission_type_id     integer,
--   ADD COLUMN IF NOT EXISTS transmission_num_speeds_id integer,
--   ADD COLUMN IF NOT EXISTS drive_type_id            integer,
--   ADD COLUMN IF NOT EXISTS body_type_id             integer,
--   ADD COLUMN IF NOT EXISTS body_num_doors_id        integer,
--   ADD COLUMN IF NOT EXISTS bed_type_id              integer,
--   ADD COLUMN IF NOT EXISTS bed_length_id            integer,
--   ADD COLUMN IF NOT EXISTS wheel_base_id            integer,
--   ADD COLUMN IF NOT EXISTS brake_system_id          integer,
--   ADD COLUMN IF NOT EXISTS brake_abs_id             integer,
--   ADD COLUMN IF NOT EXISTS steering_type_id         integer,
--   ADD COLUMN IF NOT EXISTS steering_system_id       integer,
--   ADD COLUMN IF NOT EXISTS region_id                integer;
--
-- ALTER TABLE autocare_aces_raw.app
--   ADD COLUMN IF NOT EXISTS brand_aaiaid text,
--   ADD COLUMN IF NOT EXISTS subbrand_aaiaid text,
--   ADD COLUMN IF NOT EXISTS mfr_label text;