package app.user.service;

import app.user.dto.UserProfileDto;
import app.user.request.ChangeAccountDataRequest;
import app.user.request.LoginRequest;
import app.user.request.RegisterRequest;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface UserService {

    UserProfileDto getUserByUsername(String username);

    void createUser(RegisterRequest body);

    UserProfileDto login(LoginRequest body);

    List<String> getSearchHistory(String username);

    List<String> getMessageHistory(String username);

    void changeAccountData(String username, ChangeAccountDataRequest body);

    void changeUsername(String username, String newUsername);

    void changeEmail(String username, String newEmail);

    boolean userExistsByUsername(String username);
}
