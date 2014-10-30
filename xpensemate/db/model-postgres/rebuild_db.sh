#!/usr/bin/sh
set -e
read -s -p "Password: " password
export PGPASSWORD=$password
[ "$3" == "drop" ] && echo "DROP DATABASE $2; CREATE DATABASE $2;" | psql -U $1
cat db_structure.sql db_triggers.sql db_functions.sql test_data.sql | psql -U $1 -d $2 
