package app.user.service;

import app.user.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class UserServiceImpl implements UserService {

    @Autowired
    private UserRepository userRepository;

    @Override
    public void updateData(String icon, String displayName, String description, String[] allergens) {

    }

    @Override
    public String[] getSearchHistory(String id) {
        return new String[0];
    }

    @Override
    public void updateSearchHistory(String id, String[] searchHistory) {

    }

    @Override
    public void clearSearchHistory(String id) {

    }

    @Override
    public String[] getMessageHistory(String id) {
        return new String[0];
    }

    @Override
    public void updateMessageHistory(String id, String[] messageHistory) {

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
