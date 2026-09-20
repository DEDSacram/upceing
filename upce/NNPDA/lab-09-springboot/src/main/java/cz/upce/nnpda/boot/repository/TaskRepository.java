package cz.upce.nnpda.boot.repository;

import cz.upce.nnpda.boot.entity.Task;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface TaskRepository extends JpaRepository<Task, Long> {

    List<Task> findByDone(boolean done);

    List<Task> findByTitleContainingIgnoreCase(String keyword);
}
