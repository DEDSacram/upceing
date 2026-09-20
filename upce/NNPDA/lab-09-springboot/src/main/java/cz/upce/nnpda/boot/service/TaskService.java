package cz.upce.nnpda.boot.service;

import cz.upce.nnpda.boot.config.AppProperties;
import cz.upce.nnpda.boot.dto.TaskDto;
import cz.upce.nnpda.boot.entity.Task;
import cz.upce.nnpda.boot.repository.TaskRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.NoSuchElementException;

@Service
public class TaskService {

    private final TaskRepository tasks;
    private final AppProperties properties;

    public TaskService(TaskRepository tasks, AppProperties properties) {
        this.tasks = tasks;
        this.properties = properties;
    }

    public List<TaskDto> findAll(Boolean done, String q) {
        List<Task> result;
        if (done != null) {
            result = tasks.findByDone(done);
        } else if (q != null && !q.isBlank()) {
            result = tasks.findByTitleContainingIgnoreCase(q);
        } else {
            result = tasks.findAll();
        }
        return result.stream().map(this::toDto).toList();
    }

    public TaskDto getById(Long id) {
        return toDto(require(id));
    }

    @Transactional
    public TaskDto create(TaskDto dto) {
        if (tasks.count() >= properties.getMaxTasks()) {
            throw new IllegalStateException("Task limit reached: " + properties.getMaxTasks());
        }
        Task task = new Task(dto.getTitle(), dto.getDescription());
        task.setDone(dto.isDone());
        return toDto(tasks.save(task));
    }

    @Transactional
    public TaskDto update(Long id, TaskDto dto) {
        Task task = require(id);
        task.setTitle(dto.getTitle());
        task.setDescription(dto.getDescription());
        task.setDone(dto.isDone());
        return toDto(tasks.save(task));
    }

    @Transactional
    public TaskDto toggleDone(Long id) {
        Task task = require(id);
        task.setDone(!task.isDone());
        return toDto(tasks.save(task));
    }

    @Transactional
    public void delete(Long id) {
        if (!tasks.existsById(id)) {
            throw new NoSuchElementException("Task not found: " + id);
        }
        tasks.deleteById(id);
    }

    private Task require(Long id) {
        return tasks.findById(id)
                .orElseThrow(() -> new NoSuchElementException("Task not found: " + id));
    }

    private TaskDto toDto(Task task) {
        return new TaskDto(task.getId(), task.getTitle(), task.getDescription(), task.isDone());
    }
}
