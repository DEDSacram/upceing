package cz.upce.nnpia.lab04.security;

import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

/**
 * Minimal JWT helper (HS256). In production load the secret from config/vault
 * and keep it >= 256 bits; here a fixed demo secret keeps the lab hermetic.
 */
@Component
public class JwtUtil {

    static final String SECRET = "nnpia-lab04-demo-secret-that-is-long-enough-256bit!";
    static final long EXPIRATION_MS = 3600_000;

    private SecretKey key() {
        return Keys.hmacShaKeyFor(SECRET.getBytes(StandardCharsets.UTF_8));
    }

    public String generate(String username) {
        return Jwts.builder()
                .subject(username)
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + EXPIRATION_MS))
                .signWith(key())
                .compact();
    }

    public String username(String token) {
        return Jwts.parser().verifyWith(key()).build()
                .parseSignedClaims(token).getPayload().getSubject();
    }

    public boolean valid(String token) {
        try {
            username(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }
}
