package cz.upce.nnpda.jpa;

import cz.upce.nnpda.jpa.entity.Category;
import cz.upce.nnpda.jpa.entity.Product;
import cz.upce.nnpda.jpa.repository.ProductRepository;
import jakarta.persistence.EntityManager;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

import java.math.BigDecimal;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@DataJpaTest
class ProductRepositoryTest {

    @Autowired
    private ProductRepository products;

    @Autowired
    private EntityManager entityManager;

    private Product persistSample(String productName, String categoryName,
                                  BigDecimal price, int stock) {
        Category category = new Category(categoryName);
        entityManager.persist(category);
        Product product = new Product(productName, "desc", price, stock, category);
        entityManager.persist(product);
        entityManager.flush();
        entityManager.clear();
        return product;
    }

    @Test
    void derivedQueryFindByCategoryName() {
        persistSample("Laptop", "Electronics", new BigDecimal("1000.00"), 5);
        persistSample("Novel", "Books", new BigDecimal("20.00"), 10);

        List<Product> electronics = products.findByCategoryName("Electronics");
        assertEquals(1, electronics.size());
        assertEquals("Laptop", electronics.get(0).getName());
    }

    @Test
    void derivedQueryPriceBetween() {
        persistSample("Cheap", "Cat-Cheap", new BigDecimal("10.00"), 5);
        persistSample("Mid", "Cat-Mid", new BigDecimal("50.00"), 5);
        persistSample("Expensive", "Cat-Expensive", new BigDecimal("500.00"), 5);

        List<Product> result = products.findByPriceBetween(
                new BigDecimal("5.00"), new BigDecimal("100.00"));
        assertEquals(2, result.size());
    }

    @Test
    void jpqlQueryCheapInCategory() {
        persistSample("Budget Phone", "Electronics", new BigDecimal("150.00"), 3);
        persistSample("Flagship Phone", "Electronics", new BigDecimal("1500.00"), 3);

        List<Product> cheap = products.findCheapInCategory(
                "Electronics", new BigDecimal("500.00"));
        assertEquals(1, cheap.size());
        assertEquals("Budget Phone", cheap.get(0).getName());
    }

    @Test
    void jpqlCountOutOfStock() {
        persistSample("In stock", "Cat-InStock", new BigDecimal("10.00"), 4);
        persistSample("Empty", "Cat-Empty", new BigDecimal("10.00"), 0);

        assertEquals(1, products.countOutOfStock());
    }

    @Test
    void nameSearchIsCaseInsensitive() {
        persistSample("Wireless MOUSE", "Electronics", new BigDecimal("30.00"), 7);

        List<Product> found = products.findByNameContainingIgnoreCase("mouse");
        assertTrue(found.size() >= 1);
    }
}
