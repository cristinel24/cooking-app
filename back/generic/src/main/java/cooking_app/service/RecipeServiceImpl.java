package cooking_app.service;

import cooking_app.model.recipe.Recipe;
import cooking_app.repository.RecipeRepository;

import java.util.List;

public class RecipeServiceImpl {
    private static RecipeRepository recipeRepository;
    private static RecipeServiceImpl instance;
    private RecipeServiceImpl(RecipeRepository recipeRepository) {
        RecipeServiceImpl.recipeRepository = recipeRepository;
        instance = this;
    }
    public void editRecipe(int recipeId, Recipe recipe) {
        Recipe toEdit = recipeRepository.findById(recipeId);
        toEdit.modifyRecipe(recipe);
    }
    public Recipe addRecipe(Recipe recipe) {
        return recipeRepository.saveRecipe(recipe);
    }
    public void removeRecipe(int recipeId) {
        recipeRepository.deleteById(recipeId);
    }
    public List<Recipe> fetchAll() {
        return recipeRepository.findAll();
    }
}
