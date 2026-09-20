package cz.upce.nnpia.lab01;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

/**
 * Plain JUnit 5 test — no Spring context, dependencies wired manually.
 * This is the point: constructor injection makes the class testable
 * without the container.
 */
class GreeterTest {

    private final Greeter greeter = new Greeter(new GreetingService(), new FarewellService());

    @Test
    void greetFormatsName() {
        assertEquals("Hello, NNPIA!", greeter.greet("NNPIA"));
    }

    @Test
    void partFormatsName() {
        assertEquals("Goodbye, NNPIA!", greeter.part("NNPIA"));
    }

    @Test
    void blankNameFails() {
        assertThrows(IllegalArgumentException.class, () -> greeter.greet("  "));
    }
}
