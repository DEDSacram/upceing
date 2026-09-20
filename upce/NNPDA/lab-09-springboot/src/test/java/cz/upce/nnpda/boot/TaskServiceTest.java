package cz.upce.nnpda.boot;

import cz.upce.nnpda.boot.config.AppProperties;
import cz.upce.nnpda.boot.dto.TaskDto;
import cz.upce.nnpda.boot.entity.Task;
import cz.upce.nnpda.boot.repository.TaskRepository;
import cz.upce.nnpda.boot.service.TaskService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import java.util.NoSuchElementException;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
@Transactional
class TaskServiceTest {

    @Autowired
    private TaskService service;

    @Autowired
    private TaskRepository repository;

    @Autowired
    private AppProperties properties;

    @Test
    void seedDataLoads() {
        assertTrue(repository.count() >= 2);
        assertNotNull(properties.getWelcomeMessage());
    }

    @Test
    void createAndGet() {
        TaskDto created = service.create(new TaskDto(null, "New task", "desc", false));
        assertNotNull(created.getId());

        TaskDto found = service.getById(created.getId());
        assertEquals("New task", found.getTitle());
        assertFalse(found.isDone());
    }

    @Test
    void updateAndToggle() {
        TaskDto created = service.create(new TaskDto(null, "Toggle me", null, false));

        TaskDto updated = service.update(created.getId(), new TaskDto(null, "Renamed", "x", false));
        assertEquals("Renamed", updated.getTitle());

        TaskDto toggled = service.toggleDone(created.getId());
        assertTrue(toggled.isDone());
    }

    @Test
    void deleteRemovesTask() {
        Task saved = repository.save(new Task("Temp", "to delete"));
        service.delete(saved.getId());
        assertThrows(NoSuchElementException.class, () -> service.getById(saved.getId()));
    }

    @Test
    void getMissingThrows404() {
        assertThrows(NoSuchElementException.class, () -> service.getById(999_999L));
    }
}
