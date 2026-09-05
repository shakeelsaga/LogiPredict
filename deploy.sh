#!/usr/bin/env bash
set -e

if docker compose pull web; then
  echo "Pulled prebuilt image."
else
  echo "No matching prebuilt architecture — building locally instead."
  docker compose build web
fi

docker compose up -d