package app.user.exceptions;

public class LoginError extends RuntimeException {
    public LoginError(String message) {
        super(message);
    }
}
