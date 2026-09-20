package cz.upce.nnpda.jdbc;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

import javax.sql.DataSource;

/**
 * Central database configuration.
 *
 * <p>Reads connection settings from environment variables with sensible
 * local defaults so the demo runs out of the box with docker-compose:</p>
 * <ul>
 *   <li>{@code DB_URL}  default {@code jdbc:postgresql://localhost:5432/nnpda}</li>
 *   <li>{@code DB_USER} default {@code nnpda}</li>
 *   <li>{@code DB_PASS} default {@code nnpda}</li>
 * </ul>
 */
public final class DbConfig {

    private DbConfig() {
    }

    public static String jdbcUrl() {
        return env("DB_URL", "jdbc:postgresql://localhost:5432/nnpda");
    }

    public static String username() {
        return env("DB_USER", "nnpda");
    }

    public static String password() {
        return env("DB_PASS", "nnpda");
    }

    private static String env(String name, String fallback) {
        String value = System.getenv(name);
        return (value == null || value.isBlank()) ? fallback : value;
    }

    /**
     * Creates a pooled {@link DataSource} backed by HikariCP.
     */
    public static DataSource createDataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(jdbcUrl());
        config.setUsername(username());
        config.setPassword(password());
        config.setMaximumPoolSize(5);
        config.setMinimumIdle(1);
        config.setPoolName("nnpda-pool");
        config.setAutoCommit(true);
        return new HikariDataSource(config);
    }

    /**
     * Creates a pooled {@link DataSource} for an arbitrary JDBC URL.
     * Used by tests (H2) and tooling.
     */
    public static DataSource createDataSource(String jdbcUrl, String user, String pass) {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(jdbcUrl);
        config.setUsername(user);
        config.setPassword(pass);
        config.setMaximumPoolSize(3);
        config.setMinimumIdle(1);
        config.setPoolName("nnpda-test-pool");
        return new HikariDataSource(config);
    }
}
