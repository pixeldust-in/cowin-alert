/*
This file is used to bootstrap development database.

Note: ONLY development database;
*/

CREATE ROLE cowin_alert LOGIN SUPERUSER PASSWORD 'devpassword';
ALTER ROLE vms SET client_encoding TO 'utf8';
ALTER ROLE vms SET default_transaction_isolation TO 'read committed';
ALTER ROLE vms SET timezone TO 'UTC';
CREATE DATABASE cowin_alert OWNER cowin_alert ENCODING 'utf-8';
