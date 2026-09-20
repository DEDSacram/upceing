package cz.upce.nnpda.es;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.query_dsl.Query;
import co.elastic.clients.elasticsearch.core.BulkRequest;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Hit;
import co.elastic.clients.elasticsearch.indices.CreateIndexRequest;

import java.io.StringReader;
import java.util.ArrayList;
import java.util.List;

/**
 * CRUD/search operations for the {@code products} index.
 */
public class ProductService {

    public static final String INDEX = "products";

    private final ElasticsearchClient client;

    public ProductService(ElasticsearchClient client) {
        this.client = client;
    }

    /** Deletes the index if it exists, then creates it with the given mapping JSON. */
    public void recreateIndex(String mappingJson) throws Exception {
        boolean exists = client.indices().exists(e -> e.index(INDEX)).value();
        if (exists) {
            client.indices().delete(d -> d.index(INDEX));
        }
        client.indices().create(CreateIndexRequest.of(c -> c
                .index(INDEX)
                .withJson(new StringReader(mappingJson))));
    }

    /** Bulk-indexes products; document _id = product id (idempotent re-runs). */
    public void bulkIndex(List<Product> products) throws Exception {
        BulkRequest.Builder bulk = new BulkRequest.Builder();
        for (Product p : products) {
            bulk.operations(op -> op
                    .index(idx -> idx
                            .index(INDEX)
                            .id(p.getId())
                            .document(p)));
        }
        var response = client.bulk(bulk.build());
        if (response.errors()) {
            throw new IllegalStateException("Bulk indexing reported errors");
        }
        client.indices().refresh(r -> r.index(INDEX));
    }

    /** Full-text search on an analyzed (text) field, e.g. match on "description". */
    public List<Product> searchMatch(String field, String queryText, int size) throws Exception {
        SearchResponse<Product> response = client.search(s -> s
                        .index(INDEX)
                        .size(size)
                        .query(Query.of(q -> q.match(m -> m.field(field).query(queryText)))),
                Product.class);
        return hitsToProducts(response);
    }

    /** Exact-value search on a keyword field, e.g. term on "category". */
    public List<Product> searchTerm(String field, String value, int size) throws Exception {
        SearchResponse<Product> response = client.search(s -> s
                        .index(INDEX)
                        .size(size)
                        .query(Query.of(q -> q.term(t -> t.field(field).value(value)))),
                Product.class);
        return hitsToProducts(response);
    }

    /** Simple price-range filter example. */
    public List<Product> searchPriceRange(double min, double max, int size) throws Exception {
        SearchResponse<Product> response = client.search(s -> s
                        .index(INDEX)
                        .size(size)
                        .query(Query.of(q -> q.range(r -> r
                                .field("price")
                                .gte(co.elastic.clients.json.JsonData.of(min))
                                .lte(co.elastic.clients.json.JsonData.of(max))))),
                Product.class);
        return hitsToProducts(response);
    }

    public long count() throws Exception {
        return client.count(c -> c.index(INDEX)).count();
    }

    private static List<Product> hitsToProducts(SearchResponse<Product> response) {
        List<Product> out = new ArrayList<>();
        for (Hit<Product> hit : response.hits().hits()) {
            if (hit.source() != null) {
                out.add(hit.source());
            }
        }
        return out;
    }
}
