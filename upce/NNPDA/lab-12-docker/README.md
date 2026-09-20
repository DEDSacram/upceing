# Lab 12 — Docker: Images, Containers, Volumes, Networks

No Java build required — this lab is about app virtualization.

## Theory

- **Image vs container:** image = immutable layered template;
  container = running instance of an image (image + writable layer).
- **Volumes:** persistent storage outside the container lifecycle
  (`pgdata:/var/lib/postgresql/data`). Survive `docker compose down`.
- **Networks:** compose creates an isolated bridge network; services
  resolve each other by name (`jdbc:postgresql://db:5432/demo`).
- **Layer caching:** each Dockerfile instruction = a layer. Order
  `COPY pom.xml` + dependency download before `COPY src` so code
  changes don't invalidate the dependency layer.
- **Multi-stage builds:** `maven:... AS build` compiles, final stage
  copies only the JAR onto a slim JRE — small, no JDK/Maven inside.
- **Healthchecks:** `depends_on: condition: service_healthy` waits for
  Postgres `pg_isready` before starting the app.

## Run

```bash
cd lab-12-docker
bash scripts/build.sh
bash scripts/run.sh
curl localhost:8080/api/hello
docker compose -f samples/compose-demo/docker-compose.yml --profile search up
```

## Verify

```bash
docker images lab12-demo
docker ps
docker volume ls
docker network ls
docker logs <container>
```

## Tasks

1. Build the multi-stage image, compare size with a single-stage variant.
2. Run compose (app+db), verify the app connects to `db:5432`.
3. Stop/remove containers, confirm data persists in the `pgdata` volume.
4. Enable the `search` profile, check ES on `:9200`.
5. Add a healthcheck to the app service and make nginx (lab 10) depend on it.
