-- Lab 13 example spatial queries (SRID 4326, distances in meters via unit=).

-- Cities within 25 km of Pardubice
SELECT c2.name,
       SDO_GEOM.SDO_DISTANCE(c1.geom, c2.geom, 0.005, 'unit=M') AS dist_m
FROM cities c1, cities c2
WHERE c1.name = 'Pardubice'
  AND SDO_WITHIN_DISTANCE(c2.geom, c1.geom, 'distance=25000 unit=M') = 'TRUE';

-- Topological relation of road to a city buffer
SELECT SDO_GEOM.RELATE(r.geom, c.geom, 0.005) AS rel
FROM roads r, cities c
WHERE r.name = 'I/37' AND c.name = 'Pardubice';

-- Length of road in meters
SELECT name, SDO_GEOM.SDO_LENGTH(geom, 0.005, 'unit=KM') AS len_km FROM roads;

-- Area example: 1km buffer around Pardubice
SELECT SDO_GEOM.SDO_AREA(SDO_GEOM.SDO_BUFFER(geom, 0.005, 1, 'unit=KM'), 0.005) AS area_sqkm
FROM cities WHERE name = 'Pardubice';
