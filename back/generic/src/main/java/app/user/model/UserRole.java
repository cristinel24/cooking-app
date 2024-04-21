package app.user.model;

public enum UserRole {
    USER(0b1),
    VERIFIED(0b10),
    ADMIN(0b100),
    PREMIUM(0b1000);

    private final int value;

    UserRole(int value) {
        this.value = value;
    }

    public int value() {
        return value;
    }
}
