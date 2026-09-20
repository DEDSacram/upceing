package cz.upce.nnpda.jpa.service;

import cz.upce.nnpda.jpa.entity.Category;
import cz.upce.nnpda.jpa.entity.Product;
import cz.upce.nnpda.jpa.repository.ProductRepository;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import jakarta.validation.Valid;
import org.springframework.stereotype.Service;
import org.springframework.validation.annotation.Validated;

import java.math.BigDecimal;
import java.util.List;

@Service
@Validated
public class ProductService {

    private final ProductRepository products;

    @PersistenceContext
    private EntityManager entityManager;

    public ProductService(ProductRepository products) {
        this.products = products;
    }

    public List<Product> findAll() {
        return products.findAll();
    }

    public Product getById(Long id) {
        return products.findByIdWithCategory(id)
                .orElseThrow(() -> new IllegalArgumentException("Product not found: " + id));
    }

    public List<Product> search(String keyword) {
        return products.findByNameContainingIgnoreCase(keyword);
    }

    @Transactional
    public Product create(@Valid Product product) {
        return products.save(product);
    }

    /**
     * Demonstrates a transaction spanning two writes: both succeed or both roll back.
     */
    @Transactional
    public Product createWithCategory(@Valid Product product, Category category) {
        entityManager.persist(category);
        product.setCategory(category);
        return products.save(product);
    }

    @Transactional
    public Product updatePrice(Long id, BigDecimal newPrice) {
        Product product = products.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Product not found: " + id));
        product.setPrice(newPrice); // dirty checking flushes on commit
        return product;
    }

    @Transactional
    public void delete(Long id) {
        if (!products.existsById(id)) {
            throw new IllegalArgumentException("Product not found: " + id);
        }
        products.deleteById(id);
    }
}
