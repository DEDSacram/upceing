package cz.upce.nnpia.lab01;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class App implements CommandLineRunner {

    private final Greeter greeter;

    public App(Greeter greeter) {
        this.greeter = greeter;
    }

    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }

    @Override
    public void run(String... args) {
        System.out.println(greeter.greet("NNPIA"));
        System.out.println(greeter.part("NNPIA"));
    }
}
