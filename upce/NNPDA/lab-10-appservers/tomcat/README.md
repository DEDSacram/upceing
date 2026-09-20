# Tomcat 10 deployment (WAR)

Spring Boot 3 requires Tomcat 10.1+ (Jakarta Servlet 6).

## Build WAR

```bash
# in pom.xml: <packaging>war</packaging>, tomcat scope=provided
mvn clean package
# produces target/lab10-app.war
```

## Deploy

Option A — copy to webapps:

```bash
cp target/lab10-app.war $CATALINA_HOME/webapps/
$CATALINA_HOME/bin/startup.sh
# app at http://localhost:8080/lab10-app/api/info
```

Option B — Tomcat Manager (needs a user in conf/tomcat-users.xml):

```bash
curl -u admin:admin -T target/lab10-app.war \
  "http://localhost:8080/manager/text/deploy?path=/lab10-app&update=true"
```

## Context path

- File name = context path (`lab10-app.war` -> `/lab10-app`).
- `ROOT.war` -> `/`. Remove default ROOT app first.

## Notes

- Embedded Tomcat port (`server.port`) is ignored; connector config
  lives in `conf/server.xml` (`<Connector port="8080" .../>`).
- Logs: `logs/catalina.out`.
