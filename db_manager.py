# db_manager.py

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import argparse

# --- DATABASE CONFIGURATION ---
# We will use these settings to connect to the PostgreSQL server.
# NOTE: In a real production app, you would load these from environment variables,
# not hardcode them. For our project, this is fine.

DB_CONFIG = {
    'user': 'postgres',
    'password': '123', # <--- IMPORTANT: CHANGE THIS!
    'host': 'localhost',
    'port': '5432'
}

# The name of the database we want to manage.
DB_NAME = 'anitha_hospital_db'


def connect_to_postgres_server():
    """Connects to the PostgreSQL server (not a specific database)."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        # We need to set autocommit to True to run CREATE/DROP DATABASE commands.
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Error: Could not connect to PostgreSQL server. Is it running?")
        print(f"   Details: {e}")
        return None

def create_database(cursor, db_name):
    """Creates the specified database."""
    try:
        print(f"Attempting to create database '{db_name}'...")
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"✅ Success: Database '{db_name}' created.")
    except psycopg2.errors.DuplicateDatabase:
        print(f"ℹ️ Info: Database '{db_name}' already exists.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

def drop_database(cursor, db_name):
    """Drops the specified database after confirmation."""
    confirm = input(f"⚠️  WARNING: Are you sure you want to drop the database '{db_name}'? "
                    "This action cannot be undone. [y/N]: ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        return

    try:
        print(f"Attempting to drop database '{db_name}'...")
        cursor.execute(f"DROP DATABASE {db_name}")
        print(f"✅ Success: Database '{db_name}' dropped.")
    except psycopg2.errors.InvalidCatalogName:
        print(f"ℹ️ Info: Database '{db_name}' does not exist.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="PostgreSQL Database Management Script for Anitha Hospital.")
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # 'create' command
    parser_create = subparsers.add_parser('create', help='Create the project database.')
    
    # 'drop' command
    parser_drop = subparsers.add_parser('drop', help='Drop the project database.')

    args = parser.parse_args()

    conn = connect_to_postgres_server()
    if not conn:
        return # Exit if connection failed

    cursor = conn.cursor()

    if args.command == 'create':
        create_database(cursor, DB_NAME)
    elif args.command == 'drop':
        drop_database(cursor, DB_NAME)

    # Clean up
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()