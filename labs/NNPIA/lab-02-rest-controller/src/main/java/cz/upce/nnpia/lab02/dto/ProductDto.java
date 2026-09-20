package cz.upce.nnpia.lab02.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public class ProductDto {

    public Long id;

    @NotBlank(message = "name must not be blank")
    @Size(max = 100, message = "name must be at most 100 characters")
    public String name;

    @Min(value = 0, message = "price must be >= 0")
    public int price;

    public ProductDto() {
    }

    public ProductDto(Long id, String name, int price) {
        this.id = id;
        this.name = name;
        this.price = price;
    }
}
