package app.user.model;

import app.user.providers.ExternalProvider;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.data.mongodb.core.mapping.DBRef;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class UserLoginDataExternal {
    private String providerToken;
    private ExternalProvider provider;
}
