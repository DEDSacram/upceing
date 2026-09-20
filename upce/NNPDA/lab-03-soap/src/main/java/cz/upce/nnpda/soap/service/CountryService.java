package cz.upce.nnpda.soap.service;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.stereotype.Service;

import cz.upce.nnpda.soap.model.Country;

/**
 * In-memory country repository.
 */
@Service
public class CountryService {

    private final Map<String, Country> countries = new ConcurrentHashMap<>();

    public CountryService() {
        save(new Country("Czechia", "Prague", 10800000, "CZK"));
        save(new Country("Slovakia", "Bratislava", 5400000, "EUR"));
        save(new Country("Germany", "Berlin", 83000000, "EUR"));
        save(new Country("Poland", "Warsaw", 38000000, "PLN"));
    }

    public Country findByName(String name) {
        if (name == null) {
            return null;
        }
        Country exact = countries.get(name);
        if (exact != null) {
            return exact;
        }
        // case-insensitive fallback
        for (Map.Entry<String, Country> entry : countries.entrySet()) {
            if (entry.getKey().equalsIgnoreCase(name.trim())) {
                return entry.getValue();
            }
        }
        return null;
    }

    private void save(Country country) {
        countries.put(country.getName(), country);
    }
}
