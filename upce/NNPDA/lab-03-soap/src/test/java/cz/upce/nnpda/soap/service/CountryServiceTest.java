package cz.upce.nnpda.soap.service;

import org.junit.jupiter.api.Test;

import cz.upce.nnpda.soap.model.Country;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

class CountryServiceTest {

    private final CountryService service = new CountryService();

    @Test
    void findsKnownCountry() {
        Country country = service.findByName("Czechia");
        assertNotNull(country);
        assertEquals("Prague", country.getCapital());
    }

    @Test
    void lookupIsCaseInsensitive() {
        assertNotNull(service.findByName("germany"));
    }

    @Test
    void unknownCountryReturnsNull() {
        assertNull(service.findByName("Atlantis"));
    }
}
