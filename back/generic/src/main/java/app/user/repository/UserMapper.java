package app.user.repository;

import app.user.dto.LoginDto;
import app.user.dto.UserCardDto;
import app.user.dto.UserOwnProfileDto;
import app.user.dto.UserProfileDto;
import app.user.model.User;

public class UserMapper {
    public static UserCardDto toUserCardDto(User user) {
        return new UserCardDto()
                .setIcon(user.getIcon())
                .setDisplayName(user.getDisplayName())
                .setRoles(user.getRoles())
//                .setRatings(user.getRatings())
                .setUsername(user.getUsername());
    }

    public static UserOwnProfileDto toUserOwnProfileDto(User user) {
        return new UserOwnProfileDto()
                .setIcon(user.getIcon())
                .setDisplayName(user.getDisplayName())
                .setRoles(user.getRoles())
//                .setRatings(user.getRatings())
                .setEmail(user.getEmail())
                .setUsername(user.getUsername());
    }

    public static UserProfileDto toUserProfileDto(User user) {
        return new UserProfileDto()
                .setIcon(user.getIcon())
                .setDisplayName(user.getDisplayName())
                .setRoles(user.getRoles())
//                .setRatings(user.getRatings())
                .setUsername(user.getUsername());
    }

    public static LoginDto toLoginDto(User user, String sessionToken) {
        return new LoginDto()
                .setIcon(user.getIcon())
                .setDisplayName(user.getDisplayName())
                .setRoles(user.getRoles())
                .setUsername(user.getUsername())
                .setSessionToken(sessionToken);
    }
}
