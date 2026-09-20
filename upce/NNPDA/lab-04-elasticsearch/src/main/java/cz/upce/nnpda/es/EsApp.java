package cz.upce.nnpda.es;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;

/**
 * Demo entry point: creates the index, bulk-loads sample products,
 * then runs one match query, one term query and one range query.
 *
 * <p>Run with: {@code mvn compile exec:java}</p>
 */
public class EsApp {

    public static void main(String[] args) throws Exception {
        ObjectMapper mapper = new ObjectMapper();

        String mappingJson;
        try (InputStream in = EsApp.class.getResourceAsStream("/product-mapping.json")) {
            if (in == null) {
                throw new IllegalStateException("product-mapping.json not found on classpath");
            }
            mappingJson = new String(in.readAllBytes(), StandardCharsets.UTF_8);
        }

        List<Product> products;
        try (InputStream in = EsApp.class.getResourceAsStream("/sample-products.json")) {
            if (in == null) {
                throw new IllegalStateException("sample-products.json not found on classpath");
            }
            products = mapper.readValue(in, new TypeReference<List<Product>>() {
            });
        }

        try {
            ElasticsearchClient client = EsConfig.createDefaultClient();
            try {
                ProductService service = new ProductService(client);

                System.out.println("Creating index '" + ProductService.INDEX + "' ...");
                service.recreateIndex(mappingJson);

                System.out.println("Bulk indexing " + products.size() + " products ...");
                service.bulkIndex(products);
                System.out.println("Document count: " + service.count());

                System.out.println("\n-- match query: description contains 'wireless' --");
                service.searchMatch("description", "wireless", 10).forEach(System.out::println);

                System.out.println("\n-- term query: category == 'audio' --");
                service.searchTerm("category", "audio", 10).forEach(System.out::println);

                System.out.println("\n-- range query: 50 <= price <= 200 --");
                service.searchPriceRange(50, 200, 10).forEach(System.out::println);
            } finally {
                client._transport().close();
            }
        }
    }
}
