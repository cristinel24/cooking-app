package app.user.repository;

import app.user.model.User;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends MongoRepository<User, String> {
    User findById(ObjectId id);
    User findByUsername(String username);
    User findByEmail(String email);
}
