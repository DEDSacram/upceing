# Lab 13 — Oracle Spatial

## Theory

- **SDO_GEOMETRY model:** `(GTYPE, SRID, POINT, ELEM_INFO, ORDINATES)`.
  GTYPE 2001 = point, 2002 = line; SRID 4326 = WGS84 lon/lat.
  Points use `SDO_POINT_TYPE(x, y, z)`; lines use elem-info triplets.
- **SRID 4326:** GPS coordinates; distances computed on the ellipsoid
  when `unit=M/KM` is passed to SDO functions.
- **R-tree index:** `SPATIAL_INDEX_V2` prunes candidates by bounding box
  before exact geometry tests — required for `SDO_WITHIN_DISTANCE`,
  `SDO_RELATE` performance. Metadata in `USER_SDO_GEOM_METADATA` first.
- **MapBuilder:** desktop tool to define styles/themes against a DB
  connection (connect -> create style -> create theme on table -> test).
- **MapViewer architecture:** Java EE app (WebLogic) exposing WMS/WMTS;
  themes query the `mdsys` datasource and render tiles consumed by
  OpenLayers/Leaflet. See `mapviewer/README.md`.
- **XE limitations:** 12 GB user data, 2 CPU threads, 2 GB RAM;
  Spatial is included but RAC/partitioning/tuning pack are not.

## Run

```bash
cd lab-13-oracle-spatial
docker compose up -d            # oracle-xe 21c, user spatial/spatial
# wait for DB ready (logs: "DATABASE IS READY TO USE")
mvn spring-boot:run
curl localhost:8080/api/geo/cities
xdg-open public/index.html      # OpenLayers + GeoJSON
```

## Verify

```bash
docker logs oracle 2>&1 | tail -5
docker exec -it oracle sqlplus spatial/spatial@XEPDB1 @/opt/spatial-queries.sql
curl "localhost:8080/api/geo/cities?lon=15.78&lat=50.03&dist=25000"
```

## Tasks

1. Start XE, inspect `db/spatial-schema.sql` tables and R-tree indexes.
2. Run each query in `db/spatial-queries.sql` (distance, relate, area, length).
3. Query the GeoJSON endpoint with/without `lon/lat/dist` filter.
4. Follow `mapviewer/README.md`: configure datasource, import theme XML.
5. Add a polygon table (city district), index it, query SDO_RELATE.
