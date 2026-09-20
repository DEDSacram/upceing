package cz.upce.nnpda.soap.endpoint;

import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

import cz.upce.nnpda.soap.model.Country;
import cz.upce.nnpda.soap.model.GetCountryRequest;
import cz.upce.nnpda.soap.model.GetCountryResponse;
import cz.upce.nnpda.soap.service.CountryService;

/**
 * SOAP endpoint serving {@code getCountryRequest} messages.
 */
@Endpoint
public class CountryEndpoint {

    public static final String NAMESPACE_URI = "http://upce.cz/nnpda/countries";

    private final CountryService service;

    public CountryEndpoint(CountryService service) {
        this.service = service;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getCountryRequest")
    @ResponsePayload
    public GetCountryResponse getCountry(@RequestPayload GetCountryRequest request) {
        Country country = service.findByName(request.getName());
        if (country == null) {
            // Returning an empty country keeps the contract simple for the lab;
            // a production service would throw a @SoapFault-mapped exception.
            country = new Country(request.getName(), "unknown", 0, "unknown");
        }
        return new GetCountryResponse(country);
    }
}
