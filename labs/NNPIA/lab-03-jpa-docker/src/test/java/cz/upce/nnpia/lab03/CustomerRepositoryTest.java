package cz.upce.nnpia.lab03;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@DataJpaTest
class CustomerRepositoryTest {

    @Autowired
    private CustomerRepository repo;

    @Test
    void saveAndFindByEmail() {
        repo.save(new Customer("Ada", "ada@example.com"));

        assertTrue(repo.findByEmail("ada@example.com").isPresent());
        assertEquals(1, repo.count());
    }

    @Test
    void findByEmailEmptyWhenMissing() {
        assertTrue(repo.findByEmail("nobody@example.com").isEmpty());
    }
}
