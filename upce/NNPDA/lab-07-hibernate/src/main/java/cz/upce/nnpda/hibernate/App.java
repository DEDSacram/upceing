package cz.upce.nnpda.hibernate;

import cz.upce.nnpda.hibernate.dao.BookDao;
import cz.upce.nnpda.hibernate.entity.Author;
import cz.upce.nnpda.hibernate.entity.Book;
import org.hibernate.Session;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

/**
 * Demo application: CRUD + HQL + N+1 illustration.
 *
 * Run with: mvn compile exec:java
 */
public class App {

    private static final Logger LOG = LoggerFactory.getLogger(App.class);

    public static void main(String[] args) {
        BookDao dao = new BookDao(HibernateUtil.getSessionFactory());
        try {
            // --- CREATE ---
            Author orwell = new Author("George Orwell", "United Kingdom");
            orwell.addBook(new Book("1984", 1949, 299.0));
            orwell.addBook(new Book("Animal Farm", 1945, 249.0));
            dao.saveAuthor(orwell);
            LOG.info("Saved {}", orwell);

            Author tolkien = new Author("J.R.R. Tolkien", "United Kingdom");
            tolkien.addBook(new Book("The Hobbit", 1937, 349.0));
            dao.saveAuthor(tolkien);

            // --- READ ---
            LOG.info("Total books: {}", dao.countBooks());
            List<Book> all = dao.findAllWithAuthors();
            for (Book b : all) {
                LOG.info("{} by {}", b, b.getAuthor().getName());
            }

            // --- HQL with parameter ---
            List<Book> orwellBooks = dao.findByAuthorName("George Orwell");
            LOG.info("Books by Orwell: {}", orwellBooks.size());

            // --- UPDATE (persistent state + dirty checking) ---
            Book first = all.get(0);
            dao.updatePrice(first.getId(), first.getPrice() + 10);
            LOG.info("Updated price of id={}", first.getId());

            // --- Entity states demo: transient -> persistent -> detached -> removed ---
            demonstrateEntityStates();

            // --- N+1 note ---
            LOG.info("Naive find issues 1 + N selects, JOIN FETCH issues 1 select. See README.");
            dao.findAllNaive();
            dao.findAllWithAuthors();

            // --- DELETE ---
            dao.deleteBook(first.getId());
            LOG.info("Deleted book id={}, remaining={}", first.getId(), dao.countBooks());
        } finally {
            HibernateUtil.shutdown();
        }
    }

    private static void demonstrateEntityStates() {
        // TRANSIENT: new object, unknown to Hibernate
        Book transientBook = new Book("Transient Tales", 2024, 199.0);
        LOG.info("TRANSIENT: {}", transientBook);

        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            session.beginTransaction();
            Author author = session.createQuery("from Author a", Author.class)
                    .setMaxResults(1).uniqueResult();
            transientBook.setAuthor(author);
            // PERSISTENT: attached to session after persist()
            session.persist(transientBook);
            LOG.info("PERSISTENT (id assigned on flush): {}", transientBook.getId());
            session.getTransaction().commit();
        }
        // DETACHED: session closed, object still has an id but is not managed
        LOG.info("DETACHED: {}", transientBook);
        transientBook.setPrice(210.0); // change is NOT tracked while detached

        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            session.beginTransaction();
            // merge() re-attaches the detached instance -> managed copy
            Book managed = (Book) session.merge(transientBook);
            LOG.info("Re-attached via merge: {}", managed);
            // REMOVED: marked for deletion
            session.remove(managed);
            session.getTransaction().commit();
            LOG.info("REMOVED and deleted from DB.");
        }
    }
}
