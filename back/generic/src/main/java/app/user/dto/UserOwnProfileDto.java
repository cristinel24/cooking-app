package app.user.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import app.rating.model.Rating;
import app.recipe.model.Recipe;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.Accessors;

@Getter
@Setter
@Accessors(chain = true)
@NoArgsConstructor
@ToString
@JsonInclude(value = JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class UserOwnProfileDto {
    private String icon;
    private String displayName;
    private int roles;
    private String description;
    private String username;
    private String email;
    private Recipe[] recipes;
    private Recipe[] savedRecipes;
    private Rating[] ratings;
    private String[] allergens;
}