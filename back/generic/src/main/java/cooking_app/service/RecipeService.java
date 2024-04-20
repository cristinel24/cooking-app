package cooking_app.service;

import cooking_app.model.recipe.Recipe;
import cooking_app.repository.RecipeRepository;

import java.util.List;

public interface RecipeService {
    void editRecipe(int recipeId, Recipe recipe);
    Recipe addRecipe(Recipe recipe);
    void removeRecipe(int recipeId);
    List<Recipe> fetchAll();
}
