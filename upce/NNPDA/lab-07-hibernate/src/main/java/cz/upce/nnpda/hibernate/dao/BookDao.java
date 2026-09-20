package cz.upce.nnpda.hibernate.dao;

import cz.upce.nnpda.hibernate.entity.Author;
import cz.upce.nnpda.hibernate.entity.Book;
import org.hibernate.Session;
import org.hibernate.SessionFactory;

import java.util.List;

/**
 * Simple DAO demonstrating CRUD + HQL.
 */
public class BookDao {

    private final SessionFactory sessionFactory;

    public BookDao(SessionFactory sessionFactory) {
        this.sessionFactory = sessionFactory;
    }

    public Long saveAuthor(Author author) {
        try (Session session = sessionFactory.openSession()) {
            session.beginTransaction();
            session.persist(author);
            session.getTransaction().commit();
            return author.getId();
        }
    }

    public Long saveBook(Book book) {
        try (Session session = sessionFactory.openSession()) {
            session.beginTransaction();
            session.persist(book);
            session.getTransaction().commit();
            return book.getId();
        }
    }

    public Book findBookById(Long id) {
        try (Session session = sessionFactory.openSession()) {
            return session.get(Book.class, id);
        }
    }

    public List<Book> findAll() {
        try (Session session = sessionFactory.openSession()) {
            return session.createQuery("from Book b order by b.title", Book.class).list();
        }
    }

    /** HQL with a named parameter. */
    public List<Book> findByAuthorName(String authorName) {
        try (Session session = sessionFactory.openSession()) {
            return session.createQuery(
                            "from Book b where b.author.name = :name order by b.year", Book.class)
                    .setParameter("name", authorName)
                    .list();
        }
    }

    /** HQL with JOIN FETCH to avoid the N+1 select problem (see README). */
    public List<Book> findAllWithAuthors() {
        try (Session session = sessionFactory.openSession()) {
            return session.createQuery(
                            "select b from Book b join fetch b.author order by b.title", Book.class)
                    .list();
        }
    }

    /** Naive version: triggers N+1 selects when callers touch b.getAuthor(). */
    public List<Book> findAllNaive() {
        try (Session session = sessionFactory.openSession()) {
            List<Book> books = session.createQuery("from Book b", Book.class).list();
            // Touching the lazy association here (inside session) still issues 1+N selects.
            for (Book b : books) {
                b.getAuthor().getName();
            }
            return books;
        }
    }

    public void updatePrice(Long bookId, double newPrice) {
        try (Session session = sessionFactory.openSession()) {
            session.beginTransaction();
            Book book = session.get(Book.class, bookId);
            if (book == null) {
                session.getTransaction().rollback();
                throw new IllegalArgumentException("Book not found: " + bookId);
            }
            book.setPrice(newPrice); // persistent entity -> dirty checking on commit
            session.getTransaction().commit();
        }
    }

    public void deleteBook(Long bookId) {
        try (Session session = sessionFactory.openSession()) {
            session.beginTransaction();
            Book book = session.get(Book.class, bookId);
            if (book != null) {
                session.remove(book);
            }
            session.getTransaction().commit();
        }
    }

    public long countBooks() {
        try (Session session = sessionFactory.openSession()) {
            return session.createQuery("select count(b) from Book b", Long.class).uniqueResult();
        }
    }
}
