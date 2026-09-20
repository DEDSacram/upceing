package cz.upce.nnpia.lab01;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Demonstrates IoC + constructor injection. The container creates the
 * services (beans) and injects them here — this class never calls {@code new}.
 */
@Component
public class Greeter {

    private final GreetingService greetingService;
    private final FarewellService farewellService;

    @Autowired
    public Greeter(GreetingService greetingService, FarewellService farewellService) {
        this.greetingService = greetingService;
        this.farewellService = farewellService;
    }

    public String greet(String name) {
        return greetingService.greet(name);
    }

    public String part(String name) {
        return farewellService.sayGoodbye(name);
    }
}
