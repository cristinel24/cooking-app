package app.user.service;

import app.user.dto.LoginDto;
import app.user.dto.UserProfileDto;
import app.user.request.LoginRequest;
import app.user.request.RegisterRequest;
import org.springframework.stereotype.Service;

@Service
public interface UserService {
    UserProfileDto getUserByUsername(String username);

    void createUser(RegisterRequest body);

    LoginDto login(LoginRequest body);
}
