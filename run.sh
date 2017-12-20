#!/usr/bin/env bash
set -euo pipefail

#### USAGE and ARGUMENT CHECKING
usage()
{
  echo "'run.sh' helps you to run the platform

Usage:
  run.sh install
  run.sh data
  run.sh reset
  run.sh superset
  run.sh -h|--help

Options:
  -h, --help    Display usage and exit

Commands:
  install           Initiate '.env' file. Pull / build all Docker images if they have changed.
  data              Download data, clean it and load it to postgres
  superset          Start Superset
  reset [service]   Reset all services, or selected service. Ie remove volumes data and containers
"
  exit
}
if [ -z ${1+x} ]
then
  echo "Incorrect usage."; usage
fi

case $1 in
    install|data|reset|superset ) ;; #Ok, nothing needs to be done
    -h|--help ) usage;;
    * ) echo "Incorrect usage."; usage ;;
esac


#### INSTALL
if [ $1 == "install" ]
then
    if [ ! -f .env ]; then
        echo "Create '.env' file, based on template. You should modify environment values in this file."
        cp env_template .env
    else
        echo "'.env' file already exists. We do not modify it."
    fi

    docker-compose pull
    docker-compose build

    rm -rf venv
    virtualenv venv -p python3
    set +o nounset
    source venv/bin/activate
    set -o nounset
    pip install -r requirements.txt

    exit
fi

set +o nounset
source venv/bin/activate
set -o nounset


#### DATA
if [ $1 == "data" ]
then
    src/data/download_data.sh
    src/data/clean_data.py
    scr/metadata/create_sql.py
    docker-compose up -d postgres
    src/data/load_data_to_postgres.py
    exit
fi


### SUPERSET
if [ $1 == "superset" ]
then
    echo "== Starts and initialize Superset"
    docker-compose up -d superset
    docker-compose exec superset sh -c "/etc/superset/bin/init_superset.sh" > volumes/superset/data/init_logs
    echo "Superset is up at : http://localhost:8088"
    exit
fi

#### RESET
if [ $1 == "reset" ]
then
    if [ $# = 1 ]; then
        service=all
    else
        service=$2
    fi

    case ${service} in
        all|postgres|superset|redis ) ;; #Ok, nothing needs to be done
        * ) echo "Incorrect usage. We can only reset one of the following service : postgres, superset, redis"; exit;;
    esac

    while true; do
        if [ ${service} == "all" ];
        then
            echo "This WILL DELETE ALL DATA and CONTAINERS of ALL services."
        else
            echo "This WILL DELETE ALL DATA and CONTAINER of service ${service}."
        fi
        read -p "Are you sure? [y|n] : " yn
        case $yn in
            [Yy]* ) echo "yes"; break;;
            [Nn]* ) echo "Abort"; exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done

    if [ ${service} == "all" ];
    then
        docker-compose stop
        cd volumes
            rm -rf */data
        cd ..
        yes | docker-compose rm
    else
        docker-compose stop ${service}
        rm -rf volumes/${service}/data
        yes | docker-compose rm ${service}
    fi
    exit
fi