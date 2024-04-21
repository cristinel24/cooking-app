package app.utils.crypto;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTVerificationException;
import com.auth0.jwt.interfaces.DecodedJWT;
import lombok.Value;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;

public class JwtConfig {
    private static RSAPublicKey PUBLIC_KEY = null;
    private static RSAPrivateKey PRIVATE_KEY = null;
    private static final long EXPIRATION_TIME = 604800000L; // 7 days

    private JwtConfig() throws NoSuchAlgorithmException {
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA");
        keyPairGenerator.initialize(2048);
        KeyPair keyPair = keyPairGenerator.generateKeyPair();
        PRIVATE_KEY = (RSAPrivateKey) keyPair.getPrivate();
        PUBLIC_KEY = (RSAPublicKey) keyPair.getPublic();
    }

    public static String genToken(String username) throws NoSuchAlgorithmException {
        Algorithm alg = Algorithm.RSA256(PUBLIC_KEY, PRIVATE_KEY);
        return JWT.create()
                .withIssuer("cooking-app")
                .withClaim("username", username)
                .sign(alg);
    }

    public static String getUsername(String token) {
        return JWT.decode(token).getClaim("username").asString();
    }

    public static boolean verifyToken(String token) {
        try {
            Algorithm alg = Algorithm.RSA256(PUBLIC_KEY, PRIVATE_KEY);
            JWTVerifier verifier = JWT.require(alg).withIssuer("cooking-app").build();
            verifier.verify(token);
            DecodedJWT decodedToken = JWT.decode(token);
            return true;
        } catch (JWTVerificationException e) {
            return false;
        }
    }
}