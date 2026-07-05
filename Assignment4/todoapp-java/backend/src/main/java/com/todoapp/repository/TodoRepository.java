package com.todoapp.repository;

import com.todoapp.entity.Todo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface TodoRepository extends JpaRepository<Todo, Long> {
    List<Todo> findByCompleted(Boolean completed);
    void deleteByCompletedTrue();
    long countByCompletedTrue();
}
