package app.rating.model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter @Setter
@AllArgsConstructor
public class Rating {
    private int value;
    // Userul care a facut ratingul
    private int userId;
    private String comment;
}
