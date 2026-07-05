package com.todoapp.controller;
import com.todoapp.dto.TodoRequest;
import com.todoapp.dto.TodoResponse;
import com.todoapp.dto.ApiResponse;
import com.todoapp.service.TodoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping(\"/api/v1/todos\")
@CrossOrigin(origins = \"*\")
public class TodoController {
    @Autowired private TodoService todoService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<TodoResponse>>> getAll(
            @RequestParam(required=false) Boolean completed,
            @RequestParam(defaultValue=\"100\") int limit,
            @RequestParam(defaultValue=\"0\") int offset) {
        List<TodoResponse> list = todoService.getAllTodos(completed, limit, offset);
        long total = todoService.countAll(completed);
        return ResponseEntity.ok(ApiResponse.success(list, total));
    }

    @GetMapping(\"/{id}\")
    public ResponseEntity<ApiResponse<TodoResponse>> getById(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.success(todoService.getTodoById(id)));
    }

    @PostMapping
    public ResponseEntity<ApiResponse<TodoResponse>> create(@RequestBody TodoRequest req) {
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.created(todoService.createTodo(req)));
    }

    @PutMapping(\"/{id}\")
    public ResponseEntity<ApiResponse<TodoResponse>> update(@PathVariable Long id, @RequestBody TodoRequest req) {
        return ResponseEntity.ok(ApiResponse.success(todoService.updateTodo(id, req)));
    }

    @PatchMapping(\"/{id}/toggle\")
    public ResponseEntity<ApiResponse<Void>> toggle(@PathVariable Long id) {
        todoService.toggleTodo(id);
        return ResponseEntity.ok(new ApiResponse<>(200, \"Todo status toggled successfully\", null));
    }

    @DeleteMapping(\"/{id}\")
    public ResponseEntity<ApiResponse<Void>> delete(@PathVariable Long id) {
        todoService.deleteTodo(id);
        return ResponseEntity.ok(new ApiResponse<>(200, \"Todo deleted successfully\", null));
    }

    @DeleteMapping(\"/completed\")
    public ResponseEntity<ApiResponse<Void>> deleteCompleted() {
        int count = todoService.deleteCompleted();
        return ResponseEntity.ok(new ApiResponse<>(200, \"Completed todos deleted successfully\", null));
    }

    @DeleteMapping(\"/all\")
    public ResponseEntity<ApiResponse<Void>> deleteAll() {
        int count = todoService.deleteAll();
        return ResponseEntity.ok(new ApiResponse<>(200, \"All todos deleted successfully\", null));
    }
}
