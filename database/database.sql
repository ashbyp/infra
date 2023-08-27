DROP database football;

CREATE database football;

CREATE USER guest WITH encrypted password 'guest';

GRANT ALL PRIVILEGES ON DATABASE "football" TO guest;

\c football

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO guest;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO guest;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO guest;