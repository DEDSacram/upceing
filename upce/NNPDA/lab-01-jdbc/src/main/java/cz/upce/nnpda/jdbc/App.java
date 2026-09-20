package cz.upce.nnpda.jdbc;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.List;

import javax.sql.DataSource;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.zaxxer.hikari.HikariDataSource;

/**
 * Demo application: CRUD via HikariCP + PreparedStatement + a transaction example.
 *
 * <p>Run with Postgres from docker-compose, or set DB_URL/DB_USER/DB_PASS env vars.</p>
 */
public class App {

    private static final Logger LOG = LoggerFactory.getLogger(App.class);

    public static void main(String[] args) throws Exception {
        DataSource ds = DbConfig.createDataSource();
        try {
            StudentDao dao = new StudentDao(ds);
            dao.createTable();
            dao.deleteAll();

            LOG.info("=== INSERT ===");
            Student alice = dao.insert(new Student("Alice", "Novak", "alice.novak@example.com"));
            Student bob = dao.insert(new Student("Bob", "Svoboda", "bob.svoboda@example.com"));
            LOG.info("Inserted: {} and {}", alice, bob);

            LOG.info("=== FIND ALL ===");
            List<Student> all = dao.findAll();
            all.forEach(s -> LOG.info("{}", s));

            LOG.info("=== FIND BY ID ===");
            LOG.info("Found: {}", dao.findById(alice.getId()).orElseThrow());

            LOG.info("=== UPDATE ===");
            alice.setEmail("alice.n@example.com");
            dao.update(alice);
            LOG.info("After update: {}", dao.findById(alice.getId()).orElseThrow());

            LOG.info("=== TRANSACTION (commit) ===");
            transferEmailTransaction(ds, alice.getId(), "alice.tx@example.com");

            LOG.info("=== TRANSACTION (rollback demo) ===");
            rollbackDemo(ds);

            LOG.info("=== DELETE ===");
            dao.delete(bob.getId());
            LOG.info("Remaining: {}", dao.findAll());
        } finally {
            if (ds instanceof HikariDataSource hikari) {
                hikari.close();
            }
        }
    }

    /**
     * Example of an explicit transaction: update one row and commit.
     * Uses a single Connection with autoCommit disabled.
     */
    static void transferEmailTransaction(DataSource ds, long studentId, String newEmail) throws SQLException {
        try (Connection con = ds.getConnection()) {
            con.setAutoCommit(false);
            try (PreparedStatement ps = con.prepareStatement("UPDATE students SET email = ? WHERE id = ?")) {
                ps.setString(1, newEmail);
                ps.setLong(2, studentId);
                ps.executeUpdate();
                con.commit();
                LOG.info("Transaction committed for student {}", studentId);
            } catch (SQLException e) {
                con.rollback();
                LOG.error("Transaction rolled back", e);
                throw e;
            } finally {
                con.setAutoCommit(true);
            }
        }
    }

    /**
     * Shows that a failure inside a transaction rolls everything back:
     * the first insert is undone by the failing second statement.
     */
    static void rollbackDemo(DataSource ds) throws SQLException {
        try (Connection con = ds.getConnection()) {
            con.setAutoCommit(false);
            try (PreparedStatement ok = con.prepareStatement(
                         "INSERT INTO students (first_name, last_name, email) VALUES (?, ?, ?)");
                 PreparedStatement failing = con.prepareStatement(
                         "INSERT INTO students (first_name, last_name, email) VALUES (?, ?, ?)")) {
                ok.setString(1, "Will");
                ok.setString(2, "Rollback");
                ok.setString(3, "will.rollback@example.com");
                ok.executeUpdate();

                // Violates UNIQUE(email) or NOT NULL on purpose when email already exists.
                // Use a duplicate of an existing email to force failure deterministically:
                failing.setString(1, "Broken");
                failing.setString(2, "Row");
                failing.setString(3, "alice.tx@example.com"); // duplicate -> unique violation
                failing.executeUpdate();

                con.commit();
            } catch (SQLException e) {
                con.rollback();
                LOG.info("Rollback demo: rolled back as expected ({})", e.getMessage());
            } finally {
                con.setAutoCommit(true);
            }
        }
    }
}
