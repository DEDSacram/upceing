package cz.upce.nnpia.lab01;

import org.springframework.stereotype.Service;

@Service
public class FarewellService {

    public String sayGoodbye(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("name must not be blank");
        }
        return "Goodbye, " + name + "!";
    }
}
