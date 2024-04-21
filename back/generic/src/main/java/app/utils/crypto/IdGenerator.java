package app.utils.crypto;

import java.util.concurrent.atomic.AtomicLong;

public class IdGenerator {
    static AtomicLong id = new AtomicLong(1);
    private static final String alphabet = "0123456789abcdefghijklmnopqrstuvwxyz";

    static String getId() {
        return base36encode(IdGenerator.id.getAndAdd(1));
    }

    private static String base36encode(long number) {
        StringBuilder base36 = new StringBuilder();

        do {
            base36.insert(0, alphabet.charAt((int)(number % 36)));
            number /= 36;
        } while (number > 0);

        return base36.toString();
    }
}
