#! /bin/bash
PROJECT_HOME=$PWD
MIGRATIONS_DIR="$PROJECT_HOME/migrations"

if [ "`ls -A ${MIGRATIONS_DIR}`" = "" ];
then
	flask db init
	flask db migrate
	flask db upgrade
else
	echo "${MIGRATIONS_DIR} is not empty"
fi

uwsgi --ini uwsgi.ini
