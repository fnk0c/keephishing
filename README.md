**Keephishing**

**Database Schema Exemple**

    CREATE DATABASE keephishing;
    CREATE USER keephishing;
    GRANT SELECT, INSERT, UPDATE, DELETE ON keephishing.* TO 'keephishing'@'localhost' IDENTIFIED BY 'passwd';
    FLUSH PRIVILEGES;
    CREATE TABLE watchlist(client VARCHAR(20), status VARCHAR(10), website VARCHAR(50), created DATE, updated DATE, source LONGTEXT, diff TEXT;
