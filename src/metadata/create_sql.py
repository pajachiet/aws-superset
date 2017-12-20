#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine, inspect
from src.data.load_data_to_postgres import wait_for_postgres

POSTGRES_URL = "postgres://postgres@localhost"
VIEW_NAME = 'declaration'


def main():
    table_list = ['declaration_avantage', 'declaration_convention', 'declaration_remuneration']
    for table_name in table_list:
        with open('metadata/generated/create_table_{}.sql'.format(table_name), 'w') as f:
            query = get_create_table_query(table_name)
            f.write(query)

    with open('metadata/generated/create_views.sql', 'w') as f:
        query = get_union_query(table_list)
        f.write(query)


def get_create_table_query(table_name):
    df = pd.read_csv('src/metadata/raw_schema.csv')
    columns = list()
    for row in df[[table_name, 'type']].itertuples():
        if not pd.isna(row[1]):
            columns.append('\t{} {}'.format(row[1], row[2]))

    query = "CREATE TABLE {} (\n".format(table_name)
    query += ',\n'.join(columns)
    query += '\n);\n\n'
    return query


def get_union_query(table_list):
    query = "CREATE OR REPLACE VIEW {} AS (\n\n".format(VIEW_NAME)
    query += "\nUNION ALL\n\n".join([get_select_table_query(table_name) for table_name in table_list])
    query += ")"
    return query


def get_select_table_query(table_name):
    df = pd.read_csv('src/metadata/raw_schema.csv')
    df = df[df.to_keep == 1]
    columns = list()
    for row in df[[table_name, 'name']].itertuples():
        colname = row[1]
        if pd.isna(colname):
            colname = 'NULL'
        common_name = row[2]
        if colname == common_name:
            columns.append('\t{}'.format(colname))
        else:
            columns.append('\t{} as {}'.format(colname, common_name))

    query = "SELECT\n"
    query += ',\n'.join(columns)
    query += "\nFROM {}\n".format(table_name)
    return query


if __name__ == '__main__':
    main()
