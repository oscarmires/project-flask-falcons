#!/bin/bash


cd project-flask-falcons || exit 1
git fetch && git reset origin/main --hard || exit 1
docker compose -f docker-compose.prod.yml down || exit 1
docker compose -f docker-compose.prod.yml up -d --build || exit 1
