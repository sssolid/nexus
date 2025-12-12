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

-- Optional Crown schema if you want to separate your own models
CREATE SCHEMA IF NOT EXISTS crown;

-- Grant permissions for your Django user
GRANT USAGE ON SCHEMA autocare_vcdb TO postgres;
GRANT USAGE ON SCHEMA autocare_pcdb TO postgres;
GRANT USAGE ON SCHEMA autocare_padb TO postgres;
GRANT USAGE ON SCHEMA autocare_qdb TO postgres;

GRANT SELECT ON ALL TABLES IN SCHEMA autocare_vcdb TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_pcdb TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_padb TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA autocare_qdb TO postgres;

-- Ensure new tables created manually inherit permissions
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_vcdb GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_pcdb GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_padb GRANT SELECT ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA autocare_qdb GRANT SELECT ON TABLES TO postgres;

-- Crown-specific permissions (optional)
GRANT ALL PRIVILEGES ON SCHEMA crown TO postgres;

