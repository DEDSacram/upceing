package cz.upce.nnpda.jpa.repository;

import cz.upce.nnpda.jpa.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.math.BigDecimal;
import java.util.List;

public interface ProductRepository extends JpaRepository<Product, Long> {

    // --- Derived queries ---
    List<Product> findByCategoryName(String categoryName);

    List<Product> findByPriceBetween(BigDecimal min, BigDecimal max);

    List<Product> findByNameContainingIgnoreCase(String keyword);

    List<Product> findByStockLessThan(int threshold);

    // --- JPQL with @Query ---
    @Query("select p from Product p join fetch p.category where p.id = :id")
    java.util.Optional<Product> findByIdWithCategory(@Param("id") Long id);

    @Query("select p from Product p where p.category.name = :category and p.price < :maxPrice order by p.price asc")
    List<Product> findCheapInCategory(@Param("category") String category,
                                      @Param("maxPrice") BigDecimal maxPrice);

    @Query("select count(p) from Product p where p.stock = 0")
    long countOutOfStock();
}
