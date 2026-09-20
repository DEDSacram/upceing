# Lab 01 — Spring Boot + DI/IoC

Minimal Spring Boot 3 app showing Inversion of Control and constructor injection with `@Service` / `@Component` / `@Autowired`. Unit test uses plain JUnit 5, no Spring context, no DB.

## 1. Theory

- **IoC (Inversion of Control):** instead of a class creating its dependencies with `new`, the framework creates and supplies them. The class declares *what* it needs, not *how* to build it.
- **`@Service` / `@Component`:** stereotype annotations. At startup Spring scans the package, instantiates each annotated class once (a *bean*), and registers it in the application context (the IoC container).
- **`@Autowired` on a constructor:** tells Spring which beans to pass as constructor arguments. Constructor injection is preferred: dependencies are `final`, the bean is never in a half-built state, and the class stays testable with `new` in plain unit tests.
- **Testability payoff:** `GreeterTest` wires `new Greeter(new GreetingService(), new FarewellService())` by hand — no `@SpringBootTest`, no container, millisecond-fast tests. If `Greeter` used field injection, this would be impossible without reflection or Spring.

## 2. Project layout

```
lab-01-springboot-di/
  pom.xml                                   # spring-boot-starter + plain junit-jupiter
  src/main/java/cz/upce/nnpia/lab01/
    App.java                                # @SpringBootApplication + CommandLineRunner demo
    GreetingService.java                    # @Service bean
    FarewellService.java                    # @Service bean
    Greeter.java                            # @Component, constructor-injected
  src/test/java/.../GreeterTest.java        # plain JUnit, no Spring
```

## 3. Run

```bash
cd lab-01-springboot-di
mvn test          # plain JUnit, no Spring context, no DB needed
mvn spring-boot:run
# expected output:
# Hello, NNPIA!
# Goodbye, NNPIA!
```

## 4. Verify

1. `mvn test` is green (3 tests in `GreeterTest`).
2. `mvn spring-boot:run` prints the two greeting lines (proves the container wired the beans).
3. Temporarily delete `@Service` from `GreetingService` and re-run: startup fails with `NoSuchBeanDefinitionException` — proof the container performs the wiring.

## 5. Tasks

1. Add a `TimeService` (`@Service`) returning `LocalTime.now()` and inject it into `Greeter` as `greetWithTime()`; update the test with a hand-built instance.
2. Change `Greeter` to field injection (`@Autowired` on a field) and observe how the plain unit test breaks — then revert and note why constructor injection won.
3. Add a `@Bean` method in `App` producing a `String appName` and inject it into `Greeter` with `@Qualifier` or `@Value`; explain `@Component` vs `@Bean` in a comment.
4. Write a second test that passes a stub (anonymous subclass) of `GreetingService` to prove the dependency can be swapped.
