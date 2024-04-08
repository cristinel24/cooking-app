package cooking_app;

import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class CookingAppMain {
    public static void main(String[] args) {
        SpringApplication.run(CookingAppMain.class, args);
    }

    @Bean
    ApplicationRunner init() {
        return args -> {
            Testing testing = new Testing();
        };
    }
}
