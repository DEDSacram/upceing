package cz.upce.nnpda.soap.model;

import jakarta.xml.bind.annotation.XmlAccessType;
import jakarta.xml.bind.annotation.XmlAccessorType;
import jakarta.xml.bind.annotation.XmlElement;
import jakarta.xml.bind.annotation.XmlType;

/**
 * Hand-written JAXB class mirroring the {@code country} complex type in countries.xsd.
 * (Avoids a jaxb2 code-generation plugin to keep the build simple.)
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "country", propOrder = {"name", "capital", "population", "currency"})
public class Country {

    @XmlElement(required = true)
    private String name;

    @XmlElement(required = true)
    private String capital;

    private int population;

    @XmlElement(required = true)
    private String currency;

    public Country() {
    }

    public Country(String name, String capital, int population, String currency) {
        this.name = name;
        this.capital = capital;
        this.population = population;
        this.currency = currency;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCapital() {
        return capital;
    }

    public void setCapital(String capital) {
        this.capital = capital;
    }

    public int getPopulation() {
        return population;
    }

    public void setPopulation(int population) {
        this.population = population;
    }

    public String getCurrency() {
        return currency;
    }

    public void setCurrency(String currency) {
        this.currency = currency;
    }
}
