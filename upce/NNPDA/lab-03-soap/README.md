# Lab 03 — SOAP Web Service (Spring-WS)

Contract-first SOAP service answering `getCountryRequest` with country data. Hand-written JAXB classes keep the build simple (no codegen plugin).

## 1. Theory

- **SOAP vs REST:**
  - REST: resource URLs + HTTP verbs + JSON, lightweight, WSDL-free.
  - SOAP: XML envelopes over HTTP (or JMS etc.), strict contract, built-in standards for security/reliability. Heavier but explicit.
- **WSDL** (Web Services Description Language): XML describing operations, messages, endpoint address. Generated here from the XSD by Spring-WS.
- **XSD** (XML Schema Definition): defines message shapes. See `src/main/resources/countries.xsd` (`targetNamespace http://upce.cz/nnpda/countries`, `getCountryRequest` / `getCountryResponse`).
- **JAXB:** binds XSD types to Java (`@XmlRootElement`, `@XmlType`, ...). Classes live in `model/` and mirror the XSD by hand.
- **Endpoint:** `CountryEndpoint` routes `@PayloadRoot(namespace, localPart)` to Java code; `WebServiceConfig` publishes `/ws/*` and the WSDL.

## 2. Project layout

```
lab-03-soap/
  pom.xml
  src/main/resources/{countries.xsd,application.properties}
  src/main/java/cz/upce/nnpda/soap/
    SoapApplication.java
    config/WebServiceConfig.java
    endpoint/CountryEndpoint.java
    service/CountryService.java
    model/{Country,GetCountryRequest,GetCountryResponse,package-info}.java
```

## 3. Run

```bash
cd lab-03-soap
mvn spring-boot:run
# service on http://localhost:8082/ws
# WSDL at  http://localhost:8082/ws/countries.wsdl
```

## 4. Verify

```bash
# 1) WSDL is served
curl -s http://localhost:8082/ws/countries.wsdl | head -30

# 2) SOAP request via curl
curl -s -X POST http://localhost:8082/ws \
  -H 'Content-Type: text/xml;charset=UTF-8' \
  -H 'SOAPAction: ""' \
  -d '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cou="http://upce.cz/nnpda/countries">
        <soapenv:Header/>
        <soapenv:Body>
          <cou:getCountryRequest>
            <cou:name>Czechia</cou:name>
          </cou:getCountryRequest>
        </soapenv:Body>
      </soapenv:Envelope>'
# expect <getCountryResponse> with Prague / CZK
```

Testing with **SoapUI**: create a new SOAP project from `http://localhost:8082/ws/countries.wsdl`, open the `getCountry` sample request, set `<name>Czechia</name>` and run.

Tests:

```bash
mvn test
```

## 5. Tasks

1. Add a `getAllCountries` operation (new XSD elements + endpoint method) returning all seeded countries.
2. Return a proper SOAP Fault for unknown countries (`@SoapFault` annotation + custom exception) instead of the `unknown` placeholder.
3. Add `language` to the `country` type, update XSD + JAXB + seed data.
4. Enable request logging (`PayloadLoggingInterceptor`) and verify envelopes in the console.
5. Generate a client with `jaxb2-maven-plugin` + `spring-ws` `WebServiceTemplate` and write an integration test against the running endpoint.
