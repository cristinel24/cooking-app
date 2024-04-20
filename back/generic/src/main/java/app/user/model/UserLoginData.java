package app.user.model;

import app.utils.expiring_token.model.ExpiringToken;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.data.mongodb.core.index.Indexed;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class UserLoginData {
    @Indexed(unique = true)
    private String username;
    @Indexed(unique = true)
    private String email;
    private String emailStatus;
    private String hashAlgName;
    private String passHash;
    private String passSalt; // 64 bytes
    private ExpiringToken userChangeToken;
    private ExpiringToken emailChangeToken;
    private ExpiringToken passwordResetToken;
}
