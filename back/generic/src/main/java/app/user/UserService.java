package app.user;

import app.user.dto.LoginDto;
import app.utils.requests.RequestError;
import app.user.request.LoginRequest;
import app.user.dto.UserProfileDto;
import app.user.model.User;
import app.user.model.UserLoginData;
import app.user.repository.UserMapper;
import app.user.repository.UserRepository;
import app.user.request.RegisterRequest;
import app.utils.crypto.IdGenerator;
import app.utils.crypto.TokenGenerator;
import app.utils.expiring_token.model.ExpiringToken;
import app.utils.expiring_token.repository.ExpiringTokenRepository;
import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.security.crypto.bcrypt.BCrypt;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Date;

@Log4j2
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ExpiringTokenRepository expiringTokenRepository;

    public UserProfileDto getUserByUsername(String username) {
        User user = userRepository.findByUsername(username);

        if (user == null) {
            return null;
        }

        return UserMapper.toUserProfileDto(user);
    }

    public void createUser(RegisterRequest body) {
        String salt = BCrypt.gensalt(10);
        String hash = BCrypt.hashpw(body.getPassword(), salt);

        User user = new User()
                .setName(IdGenerator.getId())
                .setUsername(body.getUsername())
                .setEmail(body.getEmail())
                .setUpdatedAt(new Date())
                .setDisplayName(body.getDisplayName())
                .setLogin(new UserLoginData()
                        .setHashAlgName("BCrypt")
                        .setHash(hash)
                        .setSalt(salt)
                )
                .setMessageHistory(new ArrayList<>())
                .setSearchHistory(new ArrayList<>())
                .setAllergens(new ArrayList<>())
                .setSessions(new ArrayList<>());

        // first insert the created user in the db
        try {
            user = userRepository.save(user);
        } catch (DataIntegrityViolationException e) {
            log.error(e.getMessage());
            throw new RequestError("Validation error");
        }

        // then create the token that the user will use to verify his account
        ExpiringToken token = new ExpiringToken()
                .setValue(TokenGenerator.getToken())
                .setUserId(user.getId())
                .setType("credentialChange");
        user.getLogin().setEmailChangeToken(token);

        // then save it to the database
        try {
            expiringTokenRepository.save(token);
        } catch (DataIntegrityViolationException e) {
            log.error(e.getMessage());
            userRepository.delete(user);
            throw new RequestError("Could not create user");
        }

        // here an email should be sent to the user with the token in order to verify their account
    }

    public void verifyUser(VerifyRequest body) {

    }

    public LoginDto login(LoginRequest body) {
        User user = null;

        if (body.getUsername() != null) {
            user = userRepository.findByUsername(body.getUsername());
        } else if (body.getEmail() != null) {
            user = userRepository.findByEmail(body.getEmail());
        }

        if (user == null) {
            throw new RequestError("User does not exist");
        }

        String hash = BCrypt.hashpw(body.getPassword(), user.getLogin().getSalt());

        if (user.getLogin().getHash().equals(hash)) {
            throw new RequestError("Passwords do not match");
        }

//        try {
//            return UserMapper.toLoginDto(user, );
            return null;
//        } catch (NoSuchAlgorithmException e) {
//            throw new LoginError("Unexpected error");
//        }
    }
}
