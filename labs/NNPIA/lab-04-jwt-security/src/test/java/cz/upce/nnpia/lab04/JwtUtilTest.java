package cz.upce.nnpia.lab04;

import cz.upce.nnpia.lab04.security.JwtUtil;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
class JwtUtilTest {

    @Autowired
    private JwtUtil jwt;

    @Test
    void roundTripKeepsUsername() {
        String token = jwt.generate("ada");
        assertTrue(jwt.valid(token));
        assertEquals("ada", jwt.username(token));
    }

    @Test
    void tamperedTokenIsRejected() {
        String token = jwt.generate("ada") + "x";
        assertFalse(jwt.valid(token));
    }
}
