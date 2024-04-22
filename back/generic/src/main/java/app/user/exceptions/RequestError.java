package app.user.exceptions;

public class RequestError extends RuntimeException {
    String message;
    public RequestError(String message) {
        super(message);

    }
}
