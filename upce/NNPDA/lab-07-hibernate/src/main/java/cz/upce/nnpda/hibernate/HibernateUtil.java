package cz.upce.nnpda.hibernate;

import cz.upce.nnpda.hibernate.entity.Author;
import cz.upce.nnpda.hibernate.entity.Book;
import org.hibernate.SessionFactory;
import org.hibernate.boot.MetadataSources;
import org.hibernate.boot.registry.StandardServiceRegistry;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;

/**
 * Builds a singleton {@link SessionFactory} from {@code hibernate.cfg.xml}.
 */
public final class HibernateUtil {

    private static final SessionFactory SESSION_FACTORY = buildSessionFactory();

    private HibernateUtil() {
    }

    private static SessionFactory buildSessionFactory() {
        StandardServiceRegistry registry = new StandardServiceRegistryBuilder()
                .configure() // loads hibernate.cfg.xml from classpath
                .build();
        try {
            return new MetadataSources(registry)
                    .addAnnotatedClass(Author.class)
                    .addAnnotatedClass(Book.class)
                    .buildMetadata()
                    .buildSessionFactory();
        } catch (Exception ex) {
            StandardServiceRegistryBuilder.destroy(registry);
            throw new ExceptionInInitializerError("SessionFactory creation failed: " + ex.getMessage());
        }
    }

    public static SessionFactory getSessionFactory() {
        return SESSION_FACTORY;
    }

    public static void shutdown() {
        getSessionFactory().close();
    }
}
