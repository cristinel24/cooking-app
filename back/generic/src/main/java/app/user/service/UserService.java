package app.user.service;

import org.springframework.stereotype.Service;

@Service
public interface UserService {

    void updateData(String icon, String displayName, String description, String[] allergens);

    String[] getSearchHistory(String id);

    void updateSearchHistory(String id, String[] searchHistory);

    void clearSearchHistory(String id);

    String[] getMessageHistory(String id);

    void updateMessageHistory(String id, String[] messageHistory);

    void clearMessageHistory(String id);

    void saveRecipe(String id, String recipeId);

    void unsaveRecipe(String id, String recipeId);

    String[] getSavedRecipes(String id);
}
