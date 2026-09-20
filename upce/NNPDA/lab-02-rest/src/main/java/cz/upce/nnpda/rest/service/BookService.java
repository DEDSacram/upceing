package cz.upce.nnpda.rest.service;

import java.util.Comparator;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Service;

import cz.upce.nnpda.rest.dto.BookDto;
import cz.upce.nnpda.rest.exception.BookNotFoundException;

/**
 * Thread-safe in-memory book store.
 */
@Service
public class BookService {

    private final ConcurrentMap<Long, BookDto> store = new ConcurrentHashMap<>();
    private final AtomicLong ids = new AtomicLong(0);

    public BookService() {
        // seed data
        create(new BookDto(null, "Effective Java", "Joshua Bloch", "978-0134685991", 2018));
        create(new BookDto(null, "Clean Code", "Robert C. Martin", "978-0132350884", 2008));
    }

    public BookDto create(BookDto dto) {
        long id = ids.incrementAndGet();
        BookDto saved = new BookDto(id, dto.getTitle(), dto.getAuthor(), dto.getIsbn(), dto.getPublishedYear());
        store.put(id, saved);
        return saved;
    }

    public BookDto findById(Long id) {
        BookDto found = store.get(id);
        if (found == null) {
            throw new BookNotFoundException(id);
        }
        return found;
    }

    /**
     * Returns a page sorted by id ascending.
     */
    public List<BookDto> findAll(int page, int size) {
        if (page < 0) {
            throw new IllegalArgumentException("page must be >= 0");
        }
        if (size < 1 || size > 100) {
            throw new IllegalArgumentException("size must be between 1 and 100");
        }
        return store.values().stream()
                .sorted(Comparator.comparing(BookDto::getId))
                .skip((long) page * size)
                .limit(size)
                .toList();
    }

    public BookDto update(Long id, BookDto dto) {
        if (!store.containsKey(id)) {
            throw new BookNotFoundException(id);
        }
        BookDto updated = new BookDto(id, dto.getTitle(), dto.getAuthor(), dto.getIsbn(), dto.getPublishedYear());
        store.put(id, updated);
        return updated;
    }

    public void delete(Long id) {
        if (store.remove(id) == null) {
            throw new BookNotFoundException(id);
        }
    }

    public long count() {
        return store.size();
    }
}
