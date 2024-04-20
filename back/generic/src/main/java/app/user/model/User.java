package app.user.model;

import app.rating.model.Rating;
import app.recipe.model.Recipe;
import app.utils.expiring_token.model.ExpiringToken;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Accessors(chain = true)
@Document(collection = "user")
public class User {
    @Id
    private String id;
    private Date updatedAt;
    private String icon;
    @Indexed
    private String displayName;
    private int roles;
    private int sumRating;
    private int countRating;
    private String description;
    private UserLoginData login;
    private UserLoginDataExternal externalLogin;
    private String[] messageHistory;
    private String[] searchHistory;
    private Recipe[] recipes;
    private String[] savedRecipes;
    private Rating[] ratings;
    private String[] allergens;
    private ExpiringToken[] sessions;
}
