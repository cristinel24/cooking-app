package app.user.request;

import jakarta.validation.constraints.*;
import lombok.Getter;
import lombok.ToString;
import org.springframework.validation.annotation.Validated;

@Getter
@ToString
@Validated
public class LoginRequest {
    @Size(min=8, max=64)
    @Pattern(regexp="[A-Za-z0-9_.]+")
    private String username;
    @Email
    private String email;
    @NotNull
    @Size(min=8, max=64)
    private String password;
}
