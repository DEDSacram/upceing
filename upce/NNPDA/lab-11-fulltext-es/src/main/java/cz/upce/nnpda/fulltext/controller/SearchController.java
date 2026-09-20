package cz.upce.nnpda.fulltext.controller;

import cz.upce.nnpda.fulltext.service.SearchService;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/search")
public class SearchController {

    private final SearchService service;

    public SearchController(SearchService service) {
        this.service = service;
    }

    @GetMapping
    public List<Map<String, Object>> search(@RequestParam("q") String q) throws IOException {
        return service.search(q);
    }

    @GetMapping("/suggest")
    public List<String> suggest(@RequestParam("q") String q) throws IOException {
        return service.suggest(q);
    }
}
