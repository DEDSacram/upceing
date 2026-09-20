package cz.upce.nnpda.fulltext.service;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.query_dsl.Operator;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Highlight;
import co.elastic.clients.elasticsearch.core.search.HighlightField;
import co.elastic.clients.elasticsearch.core.search.Suggester;
import co.elastic.clients.elasticsearch.core.search.Suggestion;
import com.fasterxml.jackson.databind.JsonNode;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Service;

@Service
public class SearchService {

    private final ElasticsearchClient es;
    private static final String INDEX = "articles";

    public SearchService(ElasticsearchClient es) {
        this.es = es;
    }

    /** multi_match with fuzziness + highlight. */
    public List<Map<String, Object>> search(String q) throws IOException {
        SearchResponse<JsonNode> res = es.search(s -> s
                .index(INDEX)
                .query(qry -> qry.multiMatch(m -> m
                        .query(q)
                        .fields("title^2", "body")
                        .operator(Operator.And)
                        .fuzziness("AUTO")))
                .highlight(Highlight.of(h -> h
                        .fields("title", HighlightField.of(f -> f))
                        .fields("body", HighlightField.of(f -> f))))
                .size(10), JsonNode.class);
        List<Map<String, Object>> out = new ArrayList<>();
        res.hits().hits().forEach(h -> out.add(Map.of(
                "id", h.id(),
                "score", h.score() == null ? 0 : h.score(),
                "source", h.source(),
                "highlight", h.highlight())));
        return out;
    }

    /** Completion suggester on title_suggest field. */
    public List<String> suggest(String prefix) throws IOException {
        var res = es.search(s -> s
                .index(INDEX)
                .suggest(Suggester.of(sg -> sg.suggesters(Map.of("s", co.elastic.clients.elasticsearch.core.search.FieldSuggester.of(f -> f
                        .prefix(prefix)
                        .completion(c -> c.field("title_suggest").size(5))))))), JsonNode.class);
        List<String> out = new ArrayList<>();
        for (List<Suggestion<JsonNode>> list : res.suggest().values()) {
            for (Suggestion<JsonNode> sug : list) {
                sug.completion().options().forEach(o -> out.add(o.text()));
            }
        }
        return out;
    }
}
