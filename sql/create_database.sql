/*
This file is used to bootstrap development database.

Note: ONLY development database;
*/

CREATE ROLE cowin_alert LOGIN CREATEDB PASSWORD 'devpassword';
ALTER ROLE cowin_alert SET client_encoding TO 'utf8';
ALTER ROLE cowin_alert SET default_transaction_isolation TO 'read committed';
ALTER ROLE cowin_alert SET timezone TO 'UTC';
CREATE DATABASE cowin_alert OWNER cowin_alert ENCODING 'utf-8';
