package cz.upce.nnpia.lab04.auth;

import cz.upce.nnpia.lab04.security.JwtUtil;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@RestController
public class AuthController {

    // demo user store: username -> bcrypt hash. Replace with JPA in a real app.
    private final Map<String, String> users = new ConcurrentHashMap<>();
    private final PasswordEncoder encoder;
    private final JwtUtil jwt;

    public AuthController(PasswordEncoder encoder, JwtUtil jwt) {
        this.encoder = encoder;
        this.jwt = jwt;
    }

    @PostMapping("/auth/register")
    public Map<String, String> register(@RequestBody Map<String, String> body) {
        String u = body.get("username");
        String p = body.get("password");
        if (u == null || u.isBlank() || p == null || p.length() < 8) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "username required, password min 8 chars");
        }
        users.put(u, encoder.encode(p));
        return Map.of("username", u);
    }

    @PostMapping("/auth/login")
    public Map<String, String> login(@RequestBody Map<String, String> body) {
        String hash = users.get(body.get("username"));
        if (hash == null || !encoder.matches(body.get("password"), hash)) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "bad credentials");
        }
        return Map.of("token", jwt.generate(body.get("username")));
    }

    @GetMapping("/api/hello")
    public Map<String, String> hello() {
        return Map.of("message", "authenticated ok");
    }
}
