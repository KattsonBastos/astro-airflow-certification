#!/usr/bin/env bash
up() {
  echo "Installing Astro CLI..."
  
  curl -sSL install.astronomer.io | sudo bash -s -- v1.8.4

}

case $1 in
  up)
    up
    ;;
  *)
    echo "Usage: $0 {up}"
    ;;
esac