#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")/../samples/compose-demo"
cp -n .env.example .env || true
docker compose up --build
