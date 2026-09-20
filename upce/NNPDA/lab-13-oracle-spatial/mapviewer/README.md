# MapViewer quickstart

Oracle MapViewer renders SDO_GEOMETRY themes as map tiles (WMS/WMTS).

## Option A — MapViewer docker (with WebLogic)

MapViewer ships as a Java EE app for WebLogic. Community approach:

```bash
docker run -d --name wls -p 7001:7001 \
  -e ORACLE_PWD=welcome1 \
  container-registry.oracle.com/middleware/weblogic:14.1.1.0
# deploy $MAPVIEWER/mapviewer.ear via WLS console http://localhost:7001/console
```

Download MapViewer 12.2.1.4 from Oracle (OTN login required),
unzip to obtain `mapviewer.ear`.

## Option B — standalone quickstart

Older MapViewer versions include `mapviewer-standalone.zip`
(embedded Jetty). Check the Oracle Spatial/MapViewer download page;
if unavailable, use Option A.

## Datasource (mdsys)

In MapViewer admin (`/mapviewer/faces/admin.jspx`):

- Connection: jdbc:oracle:thin:@oracle:1521/XEPDB1, user `spatial`.
- Data source name: `mdsys` (themes below reference it).

## Theme + basemap sample (`mapviewer/cities-theme.xml`)

```xml
<theme name="CITIES" datasource="mdsys">
  <jdbc_query spatial_column="GEOM" render_style="M.CITY"
    jdbc_srid="4326">SELECT name, geom FROM cities</jdbc_query>
</theme>
```

Import via admin console, attach to a basemap, preview with
`mapviewerdemo`.

## This lab instead

`public/index.html` renders `/api/geo/cities` GeoJSON directly with
OpenLayers — no MapViewer server needed.
