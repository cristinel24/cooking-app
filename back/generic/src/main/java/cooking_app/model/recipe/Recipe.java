package cooking_app.model.recipe;

import cooking_app.model.common.*;
import lombok.Getter;
import lombok.Setter;

import java.util.*;

@Getter @Setter
public class Recipe {
    // Nu se schimba ever
    private int recipeId;
    private int authorId;

    private String title;
    private List<Ingredient> ingredients;
    private String description;
    private List<String> steps;
    private int prepTime; // in minute
    private Set<Tag> tags;
    private List<Token> tokens; // date de AI
    private List<Allergen> allergens;

    private Date dateCreated;
    private Date dateModified;

    private List<Rating> ratings;
    private int sumRating;
    private int countRating;

    public Recipe(int authorId, String title, List<Ingredient> ingredients, String desc, List<String> steps, int prepTime, List<Allergen> allergens){
        this.authorId = authorId;
        this.title = title;
        this.ingredients = ingredients;
        this.description = desc;
        this.steps = steps;
        this.prepTime = prepTime;
        this.allergens = allergens;
        this.tags = new HashSet<>();
        this.tokens = new ArrayList<>();
        this.ratings = new ArrayList<>();
        this.dateCreated = new Date();
        this.dateModified = new Date();
    }

    public void modifyRecipe(Recipe newRecipe) {
        this.title = newRecipe.getTitle();
        this.ingredients = newRecipe.getIngredients();
        this.description = newRecipe.getDescription();
        this.steps = newRecipe.getSteps();
        this.prepTime = newRecipe.getPrepTime();
        this.allergens = newRecipe.getAllergens();
        this.dateModified = new Date(); // Resetam data modificarii la data curenta
    }

    public void addRating(Rating rating) {
        this.ratings.add(rating);
        this.sumRating += (int) rating.getValue();
        this.countRating++;
    }
    public void addTag(Tag tag) {
        tags.add(tag);
    }
    public void addToken(Token token) {
        tokens.add(token);
    }
    public float getRating() {
        if (countRating == 0) {
            return 0;
        }
        return (float) sumRating / countRating;
    }
}
