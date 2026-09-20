package cz.upce.nnpia.lab02.controller;

import cz.upce.nnpia.lab02.dto.ProductDto;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.Collection;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final Map<Long, ProductDto> store = new ConcurrentHashMap<>();
    private final AtomicLong seq = new AtomicLong();

    @GetMapping
    public Collection<ProductDto> list() {
        return store.values();
    }

    @GetMapping("/{id}")
    public ProductDto get(@PathVariable long id) {
        ProductDto found = store.get(id);
        if (found == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "product not found: " + id);
        }
        return found;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ProductDto create(@Valid @RequestBody ProductDto body) {
        long id = seq.incrementAndGet();
        ProductDto saved = new ProductDto(id, body.name, body.price);
        store.put(id, saved);
        return saved;
    }
}
