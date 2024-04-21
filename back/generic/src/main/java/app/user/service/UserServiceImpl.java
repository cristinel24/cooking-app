package app.user.service;

import app.user.dto.UserProfileDto;
import app.user.model.User;
import app.user.repository.UserRepository;
import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

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

    }

    @Override
    public void clearMessageHistory(String id) {

    }

    @Override
    public void saveRecipe(String id, String recipeId) {

    }

    @Override
    public void unsaveRecipe(String id, String recipeId) {

    }

    @Override
    public String[] getSavedRecipes(String id) {
        return new String[0];
    }
}
