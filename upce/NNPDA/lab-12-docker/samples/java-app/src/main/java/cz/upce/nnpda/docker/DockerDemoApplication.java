package cz.upce.nnpda.docker;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;

@SpringBootApplication
public class DockerDemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DockerDemoApplication.class, args);
    }

    @RestController
    static class HelloController {
        @GetMapping("/api/hello")
        Map<String, String> hello() {
            return Map.of("msg", "hello from docker");
        }
    }
}
