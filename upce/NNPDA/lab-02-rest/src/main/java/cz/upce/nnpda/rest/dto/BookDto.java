package cz.upce.nnpda.rest.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

/**
 * Book data transfer object with bean validation.
 */
public class BookDto {

    private Long id;

    @NotBlank(message = "title must not be blank")
    private String title;

    @NotBlank(message = "author must not be blank")
    private String author;

    @Pattern(regexp = "^[0-9Xx-]{10,17}$", message = "isbn must look like an ISBN (digits, X and dashes)")
    private String isbn;

    @Min(value = 1450, message = "publishedYear must be >= 1450")
    @Max(value = 2100, message = "publishedYear must be <= 2100")
    private int publishedYear;

    public BookDto() {
    }

    public BookDto(Long id, String title, String author, String isbn, int publishedYear) {
        this.id = id;
        this.title = title;
        this.author = author;
        this.isbn = isbn;
        this.publishedYear = publishedYear;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public String getIsbn() {
        return isbn;
    }

    public void setIsbn(String isbn) {
        this.isbn = isbn;
    }

    public int getPublishedYear() {
        return publishedYear;
    }

    public void setPublishedYear(int publishedYear) {
        this.publishedYear = publishedYear;
    }
}
