package cooking_app;

import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class CookingAppSystemApplication {
    public static void main(String[] args) {
        SpringApplication.run(CookingAppSystemApplication.class, args);
    }

    @Bean
    ApplicationRunner init() {
        return args -> {
            Testing testing = new Testing();
        };
    }
}
