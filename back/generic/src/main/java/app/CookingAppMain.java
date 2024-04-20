package app;

import app.user.model.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.mongodb.core.MongoTemplate;


@SpringBootApplication
public class CookingAppMain {

    private static final Logger LOGGER = LoggerFactory.getLogger(CookingAppMain.class);

    public static void main(String[] args) {
        SpringApplication.run(CookingAppMain.class, args);
        LOGGER.info("Spring Boot application started.");
    }

    @Bean
    ApplicationRunner init(MongoTemplate mongoTemplate) {
        return args -> {
            try {
                User user = mongoTemplate.findById("66226029d443d189e5e5ca66", User.class);
                LOGGER.info("Successfully connected to MongoDB. Retrieved document: {}", user);
            } catch (Exception ex) {
                LOGGER.error("Failed to connect to MongoDB: {}", ex.getMessage());
            }
        };
    }
}
