package cz.upce.nnpda.jdbc;

import java.util.List;
import java.util.Optional;

import javax.sql.DataSource;

import org.h2.jdbcx.JdbcDataSource;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * DAO tests against in-memory H2, so no Postgres is required.
 */
class StudentDaoTest {

    private StudentDao dao;

    @BeforeEach
    void setUp() throws Exception {
        DataSource ds = h2DataSource();
        dao = new StudentDao(ds);
        dao.createTable();
        dao.deleteAll();
    }

    private static DataSource h2DataSource() {
        JdbcDataSource ds = new JdbcDataSource();
        // PostgreSQL compatibility mode helps BIGSERIAL/serial handling.
        ds.setURL("jdbc:h2:mem:nnpda_test;MODE=PostgreSQL;DATABASE_TO_LOWER=TRUE;DB_CLOSE_DELAY=-1");
        ds.setUser("sa");
        ds.setPassword("");
        return ds;
    }

    @Test
    void insertAndFindById() throws Exception {
        Student saved = dao.insert(new Student("Test", "User", "test.user@example.com"));

        assertNotNull(saved.getId());

        Optional<Student> found = dao.findById(saved.getId());
        assertTrue(found.isPresent());
        assertEquals("Test", found.get().getFirstName());
        assertEquals("test.user@example.com", found.get().getEmail());
    }

    @Test
    void findAllUpdateDelete() throws Exception {
        dao.insert(new Student("A", "One", "a.one@example.com"));
        dao.insert(new Student("B", "Two", "b.two@example.com"));

        List<Student> all = dao.findAll();
        assertEquals(2, all.size());

        Student first = all.get(0);
        first.setEmail("updated@example.com");
        assertTrue(dao.update(first));
        assertEquals("updated@example.com", dao.findById(first.getId()).orElseThrow().getEmail());

        assertTrue(dao.delete(first.getId()));
        assertFalse(dao.findById(first.getId()).isPresent());
        assertEquals(1, dao.findAll().size());
    }

    @Test
    void findByIdMissingReturnsEmpty() throws Exception {
        assertTrue(dao.findById(999999L).isEmpty());
    }
}
