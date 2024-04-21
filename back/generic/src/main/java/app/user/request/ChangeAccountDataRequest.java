package app.user.request;

import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.ToString;
import org.springframework.validation.annotation.Validated;

import java.util.List;

@Getter
@ToString
@Validated
public class ChangeAccountDataRequest {
    private String icon;
    @Size(min=4, max=64)
    @Pattern(regexp="[A-Za-z0-9_.]+")
    private String displayName;
    private String description;
    private List<String> allergens;
}
