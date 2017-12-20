#!/usr/bin/env bash

echo "Extracting schema from postgres database in PostgreSQL..."
./schemacrawler.sh \
-server=postgresql -host=postgres -port=5432 -user=postgres -database=${db} \
-command=schema \
-infolevel=standard \
-portablenames \
-outputformat=pdf -outputfile=/share/sql_data_model.pdf
echo "... done."
