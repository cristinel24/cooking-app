package app.utils.requests;

public class RequestError extends RuntimeException {
    String message;
    public RequestError(String message) {
        super(message);

    }
}
