package cz.upce.nnpda.es;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.json.jackson.JacksonJsonpMapper;
import co.elastic.clients.transport.ElasticsearchTransport;
import co.elastic.clients.transport.rest_client.RestClientTransport;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.http.HttpHost;

/**
 * Factory for the Elasticsearch Java client (elasticsearch-java 8.x).
 *
 * <p>Security is disabled in this lab (see docker-compose.yml), so plain HTTP
 * against localhost:9200 is sufficient.</p>
 */
public final class EsConfig {

    private EsConfig() {
    }

    public static ElasticsearchClient createClient(String host, int port) {
        org.elasticsearch.client.RestClient restClient =
                org.elasticsearch.client.RestClient.builder(new HttpHost(host, port, "http")).build();
        ElasticsearchTransport transport =
                new RestClientTransport(restClient, new JacksonJsonpMapper(new ObjectMapper()));
        return new ElasticsearchClient(transport);
    }

    public static ElasticsearchClient createDefaultClient() {
        String host = System.getenv().getOrDefault("ES_HOST", "localhost");
        int port = Integer.parseInt(System.getenv().getOrDefault("ES_PORT", "9200"));
        return createClient(host, port);
    }
}
