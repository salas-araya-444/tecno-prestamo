CREATE DATABASE tecnoprestamo_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

SHOW DATABASES;

CREATE USER 'tecnoprestamo_user'@'localhost'
IDENTIFIED BY 'TecnoPrestamo2026!';

GRANT ALL PRIVILEGES
ON tecnoprestamo_db.*
TO 'tecnoprestamo_user'@'localhost';

GRANT ALL PRIVILEGES
ON test_tecnoprestamo_db.*
TO 'tecnoprestamo_user'@'localhost';
FLUSH PRIVILEGES;
