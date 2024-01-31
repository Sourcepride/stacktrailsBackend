#!/bin/sh

function db_is_ready(){
python << END
import sys
import psycopg2
try:
    print("Connectiong to the database '$DB_NAME'")
    psycopg2.connect(dbname="$DB_NAME", user="$DB_USER", password="$DB_PASSWORD", host="$DB_HOST")
except psycopg2.OperationalError as e:
    print(e)
    sys.exit(-1)
sys.exit(0)
END
}


until db_is_ready
do
    >&2 echo "db not fully initialized sleeping 1 second"
    sleep 1
done



 >&2 echo "Postgres is up - continuing..."

exec "$@"
