package cz.upce.nnpda.spatial.dao;

import java.sql.ResultSet;
import java.util.List;
import java.util.Map;
import oracle.sql.STRUCT;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

/** Reads SDO_GEOMETRY point ordinates without extra GIS dependencies. */
@Repository
public class GeoDao {

    private final JdbcTemplate jdbc;

    public GeoDao(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public List<Map<String, Object>> nearbyCities(double lon, double lat, double distanceMeters) {
        // distance from given point
        String anchorSql = """
                SELECT name, geom FROM cities
                WHERE SDO_WITHIN_DISTANCE(geom,
                  MDSYS.SDO_GEOMETRY(2001, 4326,
                    MDSYS.SDO_POINT_TYPE(?, ?, NULL), NULL, NULL),
                  'distance=' || ? || ' unit=M') = 'TRUE'
                """;
        return jdbc.query(anchorSql, (ResultSet rs) -> {
            var list = new java.util.ArrayList<Map<String, Object>>();
            while (rs.next()) {
                double[] xy = ordinates(rs.getObject("GEOM"));
                list.add(Map.of("name", rs.getString("NAME"), "lon", xy[0], "lat", xy[1]));
            }
            return list;
        }, lon, lat, distanceMeters);
    }

    public List<Map<String, Object>> allCities() {
        return jdbc.query("SELECT name, geom FROM cities", (ResultSet rs) -> {
            var list = new java.util.ArrayList<Map<String, Object>>();
            while (rs.next()) {
                double[] xy = ordinates(rs.getObject("GEOM"));
                list.add(Map.of("name", rs.getString("NAME"), "lon", xy[0], "lat", xy[1]));
            }
            return list;
        });
    }

    /** Extracts (lon, lat) from SDO_POINT_TYPE of a point geometry. */
    static double[] ordinates(Object structObj) throws java.sql.SQLException {
        STRUCT s = (STRUCT) structObj;
        Object[] attrs = s.getAttributes();       // gtype, srid, point, elem_info, ordinates
        STRUCT point = (STRUCT) attrs[2];         // SDO_POINT_TYPE(x, y, z)
        Object[] xyz = point.getAttributes();
        return new double[]{((Number) xyz[0]).doubleValue(), ((Number) xyz[1]).doubleValue()};
    }
}
