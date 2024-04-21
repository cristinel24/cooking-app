package app.user.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.ToString;
import org.springframework.validation.annotation.Validated;

@Getter
@ToString
@Validated
public class ChangeEmailRequest {
    @NotNull
    @Email
    private String email;
}
