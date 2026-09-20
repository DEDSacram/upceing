# WildFly 30 deployment (WAR)

## Build WAR

```bash
# in pom.xml: <packaging>war</packaging>
mvn clean package
```

## Deploy via CLI

```bash
$WILDFLY_HOME/bin/standalone.sh &   # start server, management on 9990
$WILDFLY_HOME/bin/jboss-cli.sh --connect <<'EOF'
deploy /path/to/lab10-app.war --name=lab10-app.war
info
EOF
# app at http://localhost:8080/lab10-app/api/info
```

## Undeploy / redeploy

```bash
$WILDFLY_HOME/bin/jboss-cli.sh --connect "undeploy lab10-app.war"
$WILDFLY_HOME/bin/jboss-cli.sh --connect "deploy /path/to/lab10-app.war"
```

## Context path

- Default context root = WAR name (`/lab10-app`).
- Override with `WEB-INF/jboss-web.xml`:
  `<context-root>/myapp</context-root>`.

## Notes

- WildFly uses Undertow (not Tomcat); embedded `server.port` is ignored.
- Management console: http://localhost:9990 (add user via `add-user.sh`).
