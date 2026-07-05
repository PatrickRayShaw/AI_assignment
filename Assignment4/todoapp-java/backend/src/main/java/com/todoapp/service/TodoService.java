package com.todoapp.service;
import com.todoapp.entity.Todo;
import com.todoapp.repository.TodoRepository;
import com.todoapp.dto.TodoRequest;
import com.todoapp.dto.TodoResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class TodoService {
    @Autowired private TodoRepository todoRepository;
    
    public List<TodoResponse> getAllTodos(Boolean completed, int limit, int offset) {
        List<Todo> todos;
        if (completed != null) todos = todoRepository.findByCompleted(completed);
        else todos = todoRepository.findAll();
        return todos.stream().skip(offset).limit(limit).map(this::toResponse).collect(Collectors.toList());
    }
    
    public long countAll(Boolean completed) {
        if (completed != null) return todoRepository.countByCompletedTrue();
        return todoRepository.count();
    }
    
    public TodoResponse getTodoById(Long id) {
        Todo todo = todoRepository.findById(id).orElseThrow(() -> new RuntimeException("Todo not found with id " + id));
        return toResponse(todo);
    }
    
    public TodoResponse createTodo(TodoRequest req) {
        Todo todo = new Todo();
        todo.setTitle(req.getTitle());
        todo.setDescription(req.getDescription());
        todo.setPriority(req.getPriority() != null ? req.getPriority() : 0);
        todo.setDueDate(req.getDueDate());
        todo.setCompleted(false);
        return toResponse(todoRepository.save(todo));
    }
    
    public TodoResponse updateTodo(Long id, TodoRequest req) {
        Todo todo = todoRepository.findById(id).orElseThrow(() -> new RuntimeException("Todo not found"));
        if (req.getTitle() != null) todo.setTitle(req.getTitle());
        if (req.getDescription() != null) todo.setDescription(req.getDescription());
        if (req.getCompleted() != null) todo.setCompleted(req.getCompleted());
        if (req.getPriority() != null) todo.setPriority(req.getPriority());
        if (req.getDueDate() != null) todo.setDueDate(req.getDueDate());
        return toResponse(todoRepository.save(todo));
    }
    
    public void deleteTodo(Long id) { todoRepository.deleteById(id); }
    
    public void toggleTodo(Long id) {
        Todo todo = todoRepository.findById(id).orElseThrow(() -> new RuntimeException("Todo not found"));
        todo.setCompleted(!todo.getCompleted());
        todoRepository.save(todo);
    }
    
    public int deleteCompleted() { long count = todoRepository.countByCompletedTrue(); todoRepository.deleteByCompletedTrue(); return (int) count; }
    
    public int deleteAll() { long count = todoRepository.count(); todoRepository.deleteAll(); return (int) count; }
    
    private TodoResponse toResponse(Todo todo) {
        TodoResponse r = new TodoResponse();
        r.setId(todo.getId()); r.setTitle(todo.getTitle()); r.setDescription(todo.getDescription());
        r.setCompleted(todo.getCompleted()); r.setPriority(todo.getPriority()); r.setDueDate(todo.getDueDate());
        r.setCreatedAt(todo.getCreatedAt()); r.setUpdatedAt(todo.getUpdatedAt());
        return r;
    }
}
