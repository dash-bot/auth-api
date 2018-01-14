/*
 * generate_auth_tables.sql
 *
 * Created on: 2018-01-14
 *
 * Generate tables to store user data for authentication.
 *
 */


CREATE TABLE data_users (
  first_name TEXT,
  preferred_first_name TEXT NULL,
  last_name TEXT,
  created_date DATE,
  email TEXT,
  pwd_hash BYTEA,
  speech_profile_hash BYTEA
);

CREATE TABLE data_tickets (
  ticket_val_hash BYTEA,
  issued TIMESTAMP,
  expiry TIMESTAMP
);