package cz.upce.nnpda.rest.exception;

/**
 * Thrown when a book does not exist.
 */
public class BookNotFoundException extends RuntimeException {

    public BookNotFoundException(Long id) {
        super("Book not found: " + id);
    }
}
