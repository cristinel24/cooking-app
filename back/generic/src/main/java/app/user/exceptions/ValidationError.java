package app.user.exceptions;

public class ValidationError extends RuntimeException {
    public ValidationError(Throwable cause) {
        super("Validation error", cause);
    }
}
