package cz.upce.nnpda.fulltext;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.json.jackson.JacksonJsonpMapper;
import co.elastic.clients.transport.ElasticsearchTransport;
import co.elastic.clients.transport.rest_client.RestClientTransport;
import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class FulltextApplication {
    public static void main(String[] args) {
        SpringApplication.run(FulltextApplication.class, args);
    }

    @Bean(destroyMethod = "close")
    ElasticsearchClient elasticsearchClient(@Value("${es.host:localhost:9200}") String host) {
        String[] parts = host.split(":");
        RestClient rest = RestClient.builder(new HttpHost(parts[0], Integer.parseInt(parts[1]), "http")).build();
        ElasticsearchTransport transport = new RestClientTransport(rest, new JacksonJsonpMapper());
        return new ElasticsearchClient(transport);
    }
}
