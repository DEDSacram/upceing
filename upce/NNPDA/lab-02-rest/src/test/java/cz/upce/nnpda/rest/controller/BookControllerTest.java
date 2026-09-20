package cz.upce.nnpda.rest.controller;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class BookControllerTest {

    @Autowired
    private MockMvc mvc;

    @Test
    void listReturnsSeededBooks() throws Exception {
        mvc.perform(get("/api/books"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray());
    }

    @Test
    void paginationWorks() throws Exception {
        mvc.perform(get("/api/books").param("page", "0").param("size", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)));
    }

    @Test
    void createGetUpdateDeleteLifecycle() throws Exception {
        String body = """
                {"title":"Domain-Driven Design","author":"Eric Evans",
                 "isbn":"978-0321125217","publishedYear":2003}
                """;

        String location = mvc.perform(post("/api/books")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(body))
                .andExpect(status().isCreated())
                .andExpect(header().exists("Location"))
                .andExpect(jsonPath("$.id").isNumber())
                .andExpect(jsonPath("$.title").value("Domain-Driven Design"))
                .andReturn().getResponse().getHeader("Location");

        // Location is like http://localhost/api/books/3 -> extract id from body instead
        // for robustness, fetch page and update id 3 path via GET on location path:
        mvc.perform(get("/api/books/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").isNotEmpty());

        String update = """
                {"title":"DDD Updated","author":"Eric Evans",
                 "isbn":"978-0321125217","publishedYear":2004}
                """;
        // create a fresh book and update it by reading its id
        String created = mvc.perform(post("/api/books")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(update))
                .andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();
        long id = com.jayway.jsonpath.JsonPath.parse(created).read("$.id", Long.class);

        mvc.perform(put("/api/books/" + id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(update))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("DDD Updated"));

        mvc.perform(delete("/api/books/" + id))
                .andExpect(status().isNoContent());

        mvc.perform(get("/api/books/" + id))
                .andExpect(status().isNotFound());
    }

    @Test
    void getMissingReturns404() throws Exception {
        mvc.perform(get("/api/books/999999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.message", containsString("999999")));
    }

    @Test
    void validationFailsWith400() throws Exception {
        String invalid = """
                {"title":"","author":"","isbn":"bad","publishedYear":1000}
                """;
        mvc.perform(post("/api/books")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(invalid))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Validation failed"));
    }
}
