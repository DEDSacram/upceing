package cz.upce.nnpda.spatial.controller;

import cz.upce.nnpda.spatial.dao.GeoDao;
import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/geo")
public class GeoController {

    private final GeoDao dao;

    public GeoController(GeoDao dao) {
        this.dao = dao;
    }

    /** Returns cities as a GeoJSON FeatureCollection. */
    @GetMapping(value = "/cities", produces = "application/geo+json")
    public Map<String, Object> cities(
            @RequestParam(value = "lon", required = false) Double lon,
            @RequestParam(value = "lat", required = false) Double lat,
            @RequestParam(value = "dist", defaultValue = "25000") double dist) {
        List<Map<String, Object>> rows =
                (lon != null && lat != null) ? dao.nearbyCities(lon, lat, dist) : dao.allCities();
        var features = rows.stream().map(r -> Map.of(
                "type", "Feature",
                "properties", Map.of("name", r.get("name")),
                "geometry", Map.of("type", "Point",
                        "coordinates", List.of(r.get("lon"), r.get("lat"))))).toList();
        return Map.of("type", "FeatureCollection", "features", features);
    }
}
