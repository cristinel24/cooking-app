package app.user.service;

import app.user.exceptions.LoginError;
import app.user.exceptions.ValidationError;
import app.user.request.LoginRequest;
import app.utils.crypto.JwtConfig;
import app.user.dto.UserProfileDto;
import app.user.model.User;
import app.user.model.UserLoginData;
import app.user.model.UserRole;
import app.user.repository.UserMapper;
import app.user.repository.UserRepository;
import app.user.request.RegisterRequest;
import app.utils.crypto.TokenGenerator;
import app.utils.expiring_token.model.ExpiringToken;
import com.mongodb.MongoWriteException;
import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCrypt;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.Date;

@Log4j2
@Component
public class UserServiceImpl implements UserService {

    @Autowired
    private UserRepository userRepository;

    @Override
    public UserProfileDto getUserByUsername(String username) {
        User user = userRepository.findByUsername(username);

        if (user == null) {
            return null;
        }

        return UserMapper.toUserProfileDto(user);
    }

    @Override
    public void createUser(RegisterRequest body) {
        String salt = BCrypt.gensalt(10);
        String hash = BCrypt.hashpw(body.getPassword(), salt);
        ExpiringToken token = TokenGenerator.getToken();

        User user = new User()
                .setUpdatedAt(new Date())
                .setUsername(body.getUsername())
                .setEmail(body.getEmail())
                .setDisplayName(body.getDisplayName())
                .setRoles(UserRole.USER.value())
                .setSumRating(0)
                .setCountRating(0)
                .setDescription("Let me cook!")
                .setLogin(new UserLoginData()
                        .setEmailStatus("Pending")
                        .setHashAlgName("BCrypt")
                        .setHash(hash)
                        .setSalt(salt)
                        .setEmailChangeToken(token)
                )
                .setMessageHistory(new ArrayList<>())
                .setSearchHistory(new ArrayList<>())
                .setAllergens(new ArrayList<>())
                .setSessions(new ArrayList<>());

        try {
            userRepository.save(user);
        } catch (MongoWriteException e) {
            log.error(e);
            throw new ValidationError(e);
        }
    }

    @Override
    public UserProfileDto login(LoginRequest body) {
        User user = null;

        if (body.getUsername() != null) {
            user = userRepository.findByUsername(body.getUsername());
        } else if (body.getEmail() != null) {
            user = userRepository.findByEmail(body.getEmail());
        }

        if (user == null) {
            throw new LoginError("User does not exist");
        }

        String hash = BCrypt.hashpw(body.getPassword(), user.getLogin().getSalt());

        if (user.getLogin().getHash().equals(hash)) {
            throw new LoginError("Passwords do not match");
        }

//        return UserMapper.toLoginDto(user, JwtConfig.genToken(user.getUsername()));
        return null;
    }
}
