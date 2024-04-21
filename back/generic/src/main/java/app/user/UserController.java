package app.user;

import app.user.dto.UserProfileDto;
import app.user.request.*;
import app.user.service.UserService;
import app.utils.requests.RequestMessage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/user")
public class UserController {
    @Autowired
    private UserService userService;

    @GetMapping("/{username}/profile")
    public ResponseEntity<?> getUserProfile(@PathVariable String username) {
        UserProfileDto user = userService.getUserByUsername(username);
        if (user == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new RequestMessage("User not found"));
        }
        return ResponseEntity.ok(user);
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@Validated @RequestBody RegisterRequest body, BindingResult result) {
        FieldError error = result.getFieldError();
        if (error != null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new RequestMessage(error.getField() + " " + error.getDefaultMessage()));
        }

        userService.createUser(body);
        return ResponseEntity.ok(new RequestMessage("registered successfully"));
    }

    @PostMapping("/login")
    public ResponseEntity<Object> login(@Validated @RequestBody LoginRequest body, BindingResult result) {
        if (body.getEmail() == null || body.getUsername() == null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new RequestMessage("Username required"));
        }

        FieldError error = result.getFieldError();
        if (error != null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new RequestMessage(error.getField() + " " + error.getDefaultMessage()));
        }

        UserProfileDto user = userService.login(body);
        return ResponseEntity.ok(user);
    }

    @PostMapping("/{username}/change-username")
    public ResponseEntity<?> changeUsername(@Validated @RequestBody ChangeUsernameRequest body,
                                            BindingResult result,
                                            @PathVariable String username) {
        if (!userService.userExistsByUsername(username)) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new RequestMessage("User not found"));
        }

        FieldError error = result.getFieldError();

        if (error != null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new RequestMessage(error.getField() + " " + error.getDefaultMessage()));
        }

        String newUsername = body.getUsername();
        userService.changeUsername(username, newUsername);

        return ResponseEntity.ok(new RequestMessage("changed username successfully"));
    }

    @PostMapping("/{username}/change-email")
    public ResponseEntity<?> changeEmail(@Validated @RequestBody ChangeEmailRequest body,
                                         BindingResult result,
                                         @PathVariable String username) {
        if (!userService.userExistsByUsername(username)) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new RequestMessage("User not found"));
        }

        FieldError error = result.getFieldError();

        if (error != null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new RequestMessage(error.getField() + " " + error.getDefaultMessage()));
        }

        String newEmail = body.getEmail();
        userService.changeEmail(username, newEmail);

        return ResponseEntity.ok(new RequestMessage("changed email successfully"));
    }

    @PostMapping("/{username}/change-password")
    public ResponseEntity<?> changePassword(@PathVariable String username) {
        return ResponseEntity.ok("changed password of " + username);
    }

    @PatchMapping("/{username}/change-account-data")
    public ResponseEntity<?> changeAccountData(@Validated @RequestBody ChangeAccountDataRequest body,
                                               BindingResult result,
                                               @PathVariable String username) {

        FieldError error = result.getFieldError();
        if (error != null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new RequestMessage(error.getField() + " " + error.getDefaultMessage()));
        }

        userService.changeAccountData(username, body);
        return ResponseEntity.ok(new RequestMessage("changed account data successfully"));
    }

    @GetMapping("/{username}/search-history")
    public ResponseEntity<?> getSearchHistory(@PathVariable String username) {
        if (!userService.userExistsByUsername(username)) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new RequestMessage("User not found"));
        }

        List<String> searchHistory = userService.getSearchHistory(username);

        return ResponseEntity.ok(searchHistory);
    }

    @GetMapping("/{username}/message-history")
    public ResponseEntity<?> getMessageHistory(@PathVariable String username) {
        if (!userService.userExistsByUsername(username)) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new RequestMessage("User not found"));
        }

        List<String> messageHistory = userService.getMessageHistory(username);

        return ResponseEntity.ok(messageHistory);
    }
}
