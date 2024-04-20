package app.recipe.model;

import app.allergen.model.Allergen;
import app.rating.model.Rating;
import app.tag.model.Tag;
import app.user.model.User;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.bson.types.ObjectId;

import java.util.*;

@Getter
@Setter
@NoArgsConstructor
public class Recipe {
    // Nu se schimba ever
    private ObjectId recipeId;
    private User authorId;

    private Date updatedAt;

    private String title;
    private List<String> ingredients;
    private String description;
    private List<String> steps;
    private int prepTime; // in minute
    private Set<Tag> tags;
    private List<String> tokens; // date de AI
    private List<Allergen> allergens;


    private List<Rating> ratings;
    private int sumRating;
    private int countRating;

    public Recipe(User authorId, String title, List<String> ingredients, String desc, List<String> steps, int prepTime, List<Allergen> allergens){
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
        this.sumRating = 0;
        this.countRating = 0;
        this.updatedAt = new Date();
    }

    public void modifyRecipe(Recipe newRecipe) {
        this.title = newRecipe.getTitle();
        this.ingredients = newRecipe.getIngredients();
        this.description = newRecipe.getDescription();
        this.steps = newRecipe.getSteps();
        this.prepTime = newRecipe.getPrepTime();
        this.allergens = newRecipe.getAllergens();
        this.updatedAt = new Date();
    }

    public void addRating(Rating rating) {
        this.ratings.add(rating);
        this.sumRating += (int) rating.getValue();
        this.countRating++;
    }
    public void addTag(Tag tag) {
        tags.add(tag);
    }
    public void addToken(String token) {
        tokens.add(token);
    }
    public float getRating() {
        if (countRating == 0) {
            return 0;
        }
        return (float) sumRating / countRating;
    }
}
