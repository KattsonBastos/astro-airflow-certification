#!/usr/bin/env bash
up() {
  echo "Installing Astro CLI..."
 
  curl -sSL install.astronomer.io | sudo bash -s -- v1.8.4
  
  ##
  echo "Creating astro folder.."
  mkdir astro
  cd ./astro

  ## 
  echo "Initializing Astro dev component.."
  astro dev init

  ##
  echo "Starting Airflow Services"
  astro dev start --no-cache



}

case $1 in
  up)
    up
    ;;
  *)
    echo "Usage: $0 {up}"
    ;;
esac