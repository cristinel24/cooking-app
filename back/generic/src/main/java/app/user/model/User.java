package app.user.model;

import app.rating.model.Rating;
import app.recipe.model.Recipe;
import app.utils.expiring_token.model.ExpiringToken;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Accessors(chain = true)
@Document(collection = "user")
public class User {
    @Id
    private ObjectId id;
//    @Indexed(unique = true)
//    private String name;
    @Indexed(unique = true)
    private String username;
    @Indexed(unique = true)
    private String email;
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
    private List<String> messageHistory;
    private List<String> searchHistory;
//    @DBRef
//    private List<Recipe> recipes;
//    @DBRef
//    private List<Recipe> savedRecipes;
//    @DBRef
//    private List<Rating> ratings;
    private List<String> allergens;
    private List<ExpiringToken> sessions;
}
