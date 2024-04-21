package app.user.service;

import app.user.dto.UserProfileDto;
import org.springframework.stereotype.Service;

@Service
public interface UserService {
    UserProfileDto getUserByUsername(String username);


}
