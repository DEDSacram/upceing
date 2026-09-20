# Lab 10 — Application Servers (Embedded vs Standalone)

## Theory

- **Embedded server:** Spring Boot starts Tomcat/Undertow/Jetty in-process
  from a fat JAR (`java -jar app.jar`). One process = app + server.
  Simple to deploy (Docker, cloud), version pinned per app.
- **Standalone server:** Tomcat / WildFly runs independently; apps deploy
  as WAR files into `webapps/` (Tomcat) or via management CLI (WildFly).
  One server hosts many apps, shared connection pools, central admin.
- **JAR vs WAR:** JAR = self-contained, `main()` + embedded container.
  WAR = servlet archive without server, needs external container plus
  `SpringBootServletInitializer` (see `ServletInitializer.java`).
- **Threads/connectors:** embedded Tomcat default thread pool ~200
  (`server.tomcat.threads.max`), NIO connector with accept queue.
  Standalone: tune `conf/server.xml` (Tomcat) or Undertow
  `io-threads`/`worker` subsystem (WildFly) for concurrent load.
- **Graceful shutdown:** `server.shutdown=graceful` stops accepting new
  requests, finishes in-flight ones before exit (Kubernetes-friendly).

## Run

```bash
cd lab-10-appservers
mvn spring-boot:run
curl localhost:8080/api/info
```

## Verify

```bash
mvn clean package
java -jar target/lab10-app.jar
curl localhost:8080/api/info/health
docker compose up --build   # app behind nginx on :80
curl localhost/api/info
```

## Tasks

1. Run the JAR, inspect `/api/info` (JVM, threads, memory).
2. Switch `pom.xml` to WAR packaging, rebuild, deploy to Tomcat 10
   (`tomcat/README.md`) and check the `/lab10-app` context path.
3. Deploy the same WAR to WildFly 30 (`wildfly/README.md`).
4. Run `docker compose up`, query through nginx (`:80` vs `:8080`).
5. Set `server.shutdown=graceful`, send SIGTERM during a slow request,
   observe graceful completion.
