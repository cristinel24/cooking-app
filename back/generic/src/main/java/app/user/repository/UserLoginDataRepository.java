package app.user.repository;

import app.user.model.UserLoginData;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserLoginDataRepository extends MongoRepository<UserLoginData, String> {

    UserLoginData findByUsername(String username);

    UserLoginData findByEmail(String email);
}
