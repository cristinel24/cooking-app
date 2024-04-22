package app.utils.expiring_token.model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;
import nonapi.io.github.classgraph.json.Id;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;

@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
@Document(collection = "expiring_token")
public class ExpiringToken {
    @Id
    private ObjectId id;
    // these tokens are used for the following operations: email confirmation, email & password & username change and sessions
    // if an email confirmation token is active, there shouldn't be an email & password & username change token active
    // if, for example, an email change token is active, the user can not ask to change their password as well
    @Indexed
    private String value;

    private ObjectId userId;
    private String type;
    private Date createdAt;

    public ExpiringTokenEmbed toEmbedded() {
        return new ExpiringTokenEmbed(id, value, type);
    }
}
