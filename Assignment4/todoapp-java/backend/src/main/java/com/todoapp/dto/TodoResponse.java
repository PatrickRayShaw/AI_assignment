package com.todoapp.dto;
import lombok.*;
import java.time.LocalDateTime;
@Data @NoArgsConstructor @AllArgsConstructor
public class TodoResponse {
    private Long id; private String title; private String description;
    private Boolean completed; private Integer priority; private LocalDateTime dueDate;
    private LocalDateTime createdAt; private LocalDateTime updatedAt;
}
