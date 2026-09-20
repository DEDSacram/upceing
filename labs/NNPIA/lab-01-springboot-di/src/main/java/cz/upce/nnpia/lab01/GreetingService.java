package cz.upce.nnpia.lab01;

import org.springframework.stereotype.Service;

@Service
public class GreetingService {

    public String greet(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("name must not be blank");
        }
        return "Hello, " + name + "!";
    }
}
