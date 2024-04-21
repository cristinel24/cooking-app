package app.user;

import app.user.dto.UserProfileDto;
import app.user.request.LoginRequest;
import app.utils.requests.RequestMessage;
import app.user.request.RegisterRequest;
import app.user.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

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
    public ResponseEntity<?> changeUsername(@PathVariable String username) {
        return ResponseEntity.ok("changed username of " + username);
    }

    @PostMapping("/{username}/change-email")
    public ResponseEntity<?> changeEmail(@PathVariable String username) {
        return ResponseEntity.ok("changed email of " + username);
    }

    @PostMapping("/{username}/change-password")
    public ResponseEntity<?> changePassword(@PathVariable String username) {
        return ResponseEntity.ok("changed password of " + username);
    }
}
