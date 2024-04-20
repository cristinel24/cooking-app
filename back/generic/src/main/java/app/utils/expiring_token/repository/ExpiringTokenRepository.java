package app.utils.expiring_token.repository;

import app.utils.expiring_token.model.ExpiringToken;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface ExpiringTokenRepository extends MongoRepository<ExpiringToken, String> {

    ExpiringToken findByValue(String value);
}
