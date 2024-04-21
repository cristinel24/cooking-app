package app.user.request;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.ToString;
import org.springframework.validation.annotation.Validated;

@Getter
@ToString
@Validated
public class ChangeUsernameRequest {
    @NotNull
    @Size(min=8, max=64)
    @Pattern(regexp="[A-Za-z0-9_.]+")
    private String username;
}
