package com.todoapp.dto;
import lombok.*;
import java.time.LocalDateTime;
@Data @NoArgsConstructor @AllArgsConstructor
public class TodoRequest {
    private String title;
    private String description;
    private Integer priority;
    private LocalDateTime dueDate;
}
