#!/usr/bin/env python
# coding: utf-8

import os
import sys
from time import sleep, time
from sqlalchemy import create_engine, inspect
import psycopg2
import csv
from dotenv import load_dotenv
load_dotenv('CONF')

CSV_FOLDER = "data/cleaned/"
POSTGRES_URL = "postgres://postgres@localhost"


def main():
    print("-- Importing csv into PostgreSQL tables")
    print("Waiting for PostgreSQL to start")
    wait_for_postgres(POSTGRES_URL)
    load_csv_to_postgres()

    with open('metadata/generated/create_views.sql', 'r') as f:
        query = f.read()
        engine = create_engine(POSTGRES_URL)
        with engine.connect() as connection:
            connection.execute(query)


def load_csv_to_postgres():
    for csv_filename in sorted(os.listdir(CSV_FOLDER),
                               key=lambda filename: os.path.getsize(os.path.join(CSV_FOLDER, filename))
                               ):
        if not csv_filename.endswith('.csv'):
            continue
        csv_path = os.path.join(CSV_FOLDER, csv_filename)

        table_name = os.path.basename(csv_filename)[:-21]
        create_or_replace_table_in_postgres(table_name)

        size = sizeof_fmt(os.path.getsize(csv_path))
        print("{} ({}) TO table {}".format(csv_filename, size, table_name))
        start = time()
        import_csv_to_postgres_table(csv_path, table_name, POSTGRES_URL)
        elapsed = time() - start
        print("import took {:.3f} s".format(elapsed))


def import_csv_to_postgres_table(csv_path, table_name, postgres_url):
    """ Import a csv to a postgres table

    Replace table if one exists at the same place.

    :param csv_path: 
    :param postgres_url: 
    :return: 
    """

    # Guess delimiter, for use by pandas and postgres
    with open(csv_path, 'r') as csv_file:
        dialect = csv.Sniffer().sniff(csv_file.read(1024))
    sep = dialect.delimiter

    # Stream csv data into postgres, thanks to dedicated function
    print('Stream csv data into postgres')
    connection = psycopg2.connect(postgres_url)
    connection.cursor().execute("SET datestyle = 'ISO,DMY';")
    with connection.cursor() as cursor:
        with open(csv_path, 'r') as csv_file:
            csv_file.readline()
            cursor.copy_expert(
                """COPY {} FROM STDIN WITH (FORMAT CSV, DELIMITER '{}', ENCODING latin1)""".format(table_name, sep),
                csv_file
            )
    connection.commit()


def create_or_replace_table_in_postgres(table_name):
    if table_name.startswith('entreprise'):
        query_file = 'metadata/create_table_{}.sql'.format(table_name)
    else:
        query_file = 'metadata/generated/create_table_{}.sql'.format(table_name)

    with open(query_file, 'r') as f:
        query = f.read()
        engine = create_engine(POSTGRES_URL)
        with engine.connect() as connection:
            ins = inspect(engine)
            if table_name in ins.get_table_names():
                connection.execute("DROP TABLE {} CASCADE".format(table_name))
            connection.execute(query)


def wait_for_postgres(postgres_url):
    if test_connection_to_postgresql(postgres_url):
        return
    while not test_connection_to_postgresql(postgres_url):
        sys.stdout.write('.')
        sys.stdout.flush()
        sleep(1)


def test_connection_to_postgresql(postgres_url):
    """ Test if the target PostgreSQL database accept connexions
    """
    try:
        psycopg2.connect(postgres_url)
    except psycopg2.OperationalError:
        return False
    else:
        return True


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

if __name__ == '__main__':
    main()
