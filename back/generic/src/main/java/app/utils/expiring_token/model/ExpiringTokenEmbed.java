package app.utils.expiring_token.model;

import jakarta.persistence.Embeddable;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import nonapi.io.github.classgraph.json.Id;
import org.bson.types.ObjectId;

@Getter
@Setter
@AllArgsConstructor
@Embeddable
public class ExpiringTokenEmbed {
    @Id
    private ObjectId id;
    private String value;
    private String type;
}