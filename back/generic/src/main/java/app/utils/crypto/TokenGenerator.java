package app.utils.crypto;

import app.utils.expiring_token.model.ExpiringToken;

import java.security.SecureRandom;
import java.util.Date;

public class TokenGenerator {
    private static final long EXPIRATION_TIME = 604800000L; // 7 days

    public static ExpiringToken getToken() {
        byte[] bytes = new byte[20];
        new SecureRandom().nextBytes(bytes);
        return new ExpiringToken().setValue(bytesToHex(bytes)).setDate(new Date(new Date().getTime() + EXPIRATION_TIME));
    }

    private static final char[] HEX_ARRAY = "0123456789ABCDEF".toCharArray();

    private static String bytesToHex(byte[] bytes) {
        char[] hexChars = new char[bytes.length * 2];
        for (int j = 0; j < bytes.length; j++) {
            int v = bytes[j] & 0xFF;
            hexChars[j * 2] = HEX_ARRAY[v >>> 4];
            hexChars[j * 2 + 1] = HEX_ARRAY[v & 0x0F];
        }
        return new String(hexChars);
    }
}
