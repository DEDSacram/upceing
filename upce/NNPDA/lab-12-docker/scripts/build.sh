#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")/../samples/java-app"
docker build -t lab12-demo .
docker images lab12-demo
