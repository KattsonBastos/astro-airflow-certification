#!/usr/bin/env bash
up() {
  echo "Creating Container..."

  docker-compose up -d
  
  sudo chmod -R 777 dags
}

config(){
  docker exec practices-airflow-webserver-1 airflow connections add 'postgres' \
    --conn-json '{
        "conn_type": "Postgres",
        "login": "airflow",
        "password": "airflow",
        "host": "postgres",
        "port": 5432
    }'
}

case $1 in
  up)
    up
    ;;
  config)
    config
    ;;
  *)
    echo "Usage: $0 {up, config}"
    ;;
esac