-- Initialize PostgreSQL database with optimizations for Django application

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For trigram text search
CREATE EXTENSION IF NOT EXISTS "btree_gin"; -- For composite indexes

-- Create database if not exists (handled by POSTGRES_DB env var)

-- Configure PostgreSQL for better performance
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '128MB';
ALTER SYSTEM SET work_mem = '16MB';
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;
ALTER SYSTEM SET max_connections = 100;

-- Full text search configuration
ALTER DATABASE nexus SET default_text_search_config = 'pg_catalog.english';

-- Log configuration for debugging (disable in production)
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_duration = on;
ALTER SYSTEM SET log_min_duration_statement = 1000; -- Log queries taking > 1 second

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

-- Set useful default search path (optional)
ALTER DATABASE nexus SET search_path = public, crown;

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

