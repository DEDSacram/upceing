package cz.upce.nnpda.hibernate;

import cz.upce.nnpda.hibernate.dao.BookDao;
import cz.upce.nnpda.hibernate.entity.Author;
import cz.upce.nnpda.hibernate.entity.Book;
import org.hibernate.SessionFactory;
import org.hibernate.boot.MetadataSources;
import org.hibernate.boot.registry.StandardServiceRegistry;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

class BookDaoTest {

    private static SessionFactory sessionFactory;
    private BookDao dao;

    @BeforeAll
    static void initFactory() {
        Map<String, Object> settings = new HashMap<>();
        settings.put("hibernate.connection.driver_class", "org.h2.Driver");
        settings.put("hibernate.connection.url", "jdbc:h2:mem:lab07test;DB_CLOSE_DELAY=-1;MODE=PostgreSQL");
        settings.put("hibernate.connection.username", "sa");
        settings.put("hibernate.connection.password", "");
        settings.put("hibernate.dialect", "org.hibernate.dialect.H2Dialect");
        settings.put("hibernate.hbm2ddl.auto", "create-drop");
        settings.put("hibernate.show_sql", "false");

        StandardServiceRegistry registry = new StandardServiceRegistryBuilder()
                .applySettings(settings).build();
        sessionFactory = new MetadataSources(registry)
                .addAnnotatedClass(Author.class)
                .addAnnotatedClass(Book.class)
                .buildMetadata()
                .buildSessionFactory();
    }

    @AfterAll
    static void closeFactory() {
        if (sessionFactory != null) {
            sessionFactory.close();
        }
    }

    @BeforeEach
    void setUp() {
        dao = new BookDao(sessionFactory);
        // Clean tables between tests
        try (var session = sessionFactory.openSession()) {
            session.beginTransaction();
            session.createMutationQuery("delete from Book").executeUpdate();
            session.createMutationQuery("delete from Author").executeUpdate();
            session.getTransaction().commit();
        }
    }

    @Test
    void saveAndFindBook() {
        Author author = new Author("Test Author", "CZ");
        author.addBook(new Book("Test Book", 2020, 100.0));
        dao.saveAuthor(author);

        assertNotNull(author.getId());
        assertEquals(1, dao.countBooks());

        Book found = dao.findBookById(author.getBooks().get(0).getId());
        assertNotNull(found);
        assertEquals("Test Book", found.getTitle());
    }

    @Test
    void findByAuthorNameUsesHql() {
        Author a = new Author("George Orwell", "United Kingdom");
        a.addBook(new Book("1984", 1949, 299.0));
        dao.saveAuthor(a);

        Author b = new Author("Somebody Else", "CZ");
        b.addBook(new Book("Other", 2000, 150.0));
        dao.saveAuthor(b);

        List<Book> result = dao.findByAuthorName("George Orwell");
        assertEquals(1, result.size());
        assertEquals("1984", result.get(0).getTitle());
    }

    @Test
    void fetchJoinLoadsAuthors() {
        Author a = new Author("Author One", "CZ");
        a.addBook(new Book("Book A", 2001, 100.0));
        a.addBook(new Book("Book B", 2002, 200.0));
        dao.saveAuthor(a);

        List<Book> books = dao.findAllWithAuthors();
        assertEquals(2, books.size());
        for (Book book : books) {
            assertNotNull(book.getAuthor());
            assertNotNull(book.getAuthor().getName());
        }
    }

    @Test
    void updateAndDelete() {
        Author a = new Author("Author X", "CZ");
        a.addBook(new Book("Priced Book", 2010, 100.0));
        dao.saveAuthor(a);
        Long id = a.getBooks().get(0).getId();

        dao.updatePrice(id, 555.0);
        assertEquals(555.0, dao.findBookById(id).getPrice(), 0.001);

        dao.deleteBook(id);
        assertNull(dao.findBookById(id));
        assertEquals(0, dao.countBooks());
    }
}
