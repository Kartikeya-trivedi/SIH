"""Database initialization script."""

-- Create database and user
CREATE DATABASE kolam_db;
CREATE DATABASE kolam_test_db;

-- Create user
CREATE USER kolam_user WITH PASSWORD 'kolam_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE kolam_db TO kolam_user;
GRANT ALL PRIVILEGES ON DATABASE kolam_test_db TO kolam_user;

-- Connect to kolam_db and grant schema privileges
\c kolam_db;
GRANT ALL ON SCHEMA public TO kolam_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO kolam_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO kolam_user;

-- Connect to kolam_test_db and grant schema privileges
\c kolam_test_db;
GRANT ALL ON SCHEMA public TO kolam_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO kolam_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO kolam_user;

