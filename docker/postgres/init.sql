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
