package app.user;

import app.user.dto.LoginDto;
import app.user.dto.UserProfileDto;
import app.utils.requests.RequestError;
import app.user.request.LoginRequest;
import app.utils.requests.RequestMessage;
import app.user.request.RegisterRequest;
import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/user")
@Log4j2
public class UserController {
    @Autowired
    private UserService userService;

    @GetMapping("/{username}/profile")
    public ResponseEntity<?> getUserProfile(@PathVariable String username) {
        UserProfileDto user = null;
        try {
            user = userService.getUserByUsername(username);
        } catch (Exception e) {
            log.error(e);
            return ResponseEntity.badRequest().body(new RequestMessage("Internal error"));
        }

        if (user == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new RequestMessage("User not found"));
        }

        return ResponseEntity.ok(user);
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@Validated @RequestBody RegisterRequest body, BindingResult result) {
        FieldError error = result.getFieldError();
        if (error != null) {
            return ResponseEntity.badRequest().body(new RequestMessage(error.getField() + " " + error.getDefaultMessage()));
        }

        try {
            userService.createUser(body);
        } catch (RequestError e) {
            log.error(e);
            return ResponseEntity.badRequest().body(new RequestMessage(e.getMessage()));
        } catch (Exception e) {
            log.error(e);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new RequestMessage("Internal error"));
        }

        return ResponseEntity.ok(new RequestMessage("registered successfully"));
    }


    @PostMapping("/login")
    public ResponseEntity<Object> login(@Validated @RequestBody LoginRequest body, BindingResult result) {
        if (body.getEmail() == null || body.getUsername() == null) {
            return ResponseEntity.badRequest().body(new RequestMessage("Username required"));
        }

        FieldError error = result.getFieldError();
        if (error != null) {
            return ResponseEntity.badRequest().body(new RequestMessage(error.getField() + " " + error.getDefaultMessage()));
        }

        LoginDto user = null;

        try {
            user = userService.login(body);
        } catch (RequestError e) {
            log.error(e);
            return ResponseEntity.badRequest().body(new RequestMessage(e.getMessage()));
        } catch (Exception e) {
            log.error(e);
            return ResponseEntity.badRequest().body(new RequestMessage("Internal error"));
        }

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
