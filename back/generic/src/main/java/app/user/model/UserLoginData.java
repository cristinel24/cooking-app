package app.user.model;

import app.utils.expiring_token.model.ExpiringToken;
import app.utils.expiring_token.model.ExpiringTokenEmbed;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;
import org.springframework.data.mongodb.core.index.Indexed;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Accessors(chain = true)
public class UserLoginData {
    private String emailStatus = "Pending";
    private String hashAlgName;
    private String hash;
    private String salt; // 64 bytes
    private ExpiringTokenEmbed changeToken;
    private String newEmail;
}