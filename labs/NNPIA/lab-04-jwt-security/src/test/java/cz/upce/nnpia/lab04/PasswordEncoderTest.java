package cz.upce.nnpia.lab04;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;

import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
class PasswordEncoderTest {

    @Autowired
    private PasswordEncoder encoder;

    @Test
    void bcryptHashesAndVerifies() {
        String hash = encoder.encode("s3cret-pw!");
        assertNotEquals("s3cret-pw!", hash);
        assertTrue(encoder.matches("s3cret-pw!", hash));
    }
}
