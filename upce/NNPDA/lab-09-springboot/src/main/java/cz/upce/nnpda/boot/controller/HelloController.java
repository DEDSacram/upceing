package cz.upce.nnpda.boot.controller;

import cz.upce.nnpda.boot.config.AppProperties;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/api/hello")
public class HelloController {

    private final AppProperties properties;

    public HelloController(AppProperties properties) {
        this.properties = properties;
    }

    @GetMapping
    public Map<String, String> hello() {
        return Map.of("message", properties.getWelcomeMessage());
    }
}
