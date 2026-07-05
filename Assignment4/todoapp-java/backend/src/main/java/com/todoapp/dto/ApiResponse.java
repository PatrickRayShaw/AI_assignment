package com.todoapp.dto;
import lombok.*;
@Data @NoArgsConstructor @AllArgsConstructor
public class ApiResponse<T> {
    private int code; private String message; private T data; private Long total; private Integer deletedCount;
    public ApiResponse(int code, String message, T data) { this.code=code; this.message=message; this.data=data; }
    public static <T> ApiResponse<T> success(T data) { return new ApiResponse<>(200,"success",data); }
    public static <T> ApiResponse<T> success(T data, long total) { ApiResponse<T> r = new ApiResponse<>(200,"success",data); r.total=total; return r; }
    public static <T> ApiResponse<T> created(T data) { return new ApiResponse<>(201,"Todo created successfully",data); }
    public static <T> ApiResponse<T> deleted(int count) { ApiResponse<T> r = new ApiResponse<>(200,"Deleted successfully",null); r.deletedCount=count; return r; }
    public static <T> ApiResponse<T> error(int code, String msg) { return new ApiResponse<>(code,msg,null); }
}
