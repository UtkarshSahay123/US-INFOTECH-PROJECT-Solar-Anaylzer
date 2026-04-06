package com.example.demo.security;

import com.example.demo.models.User;
import com.example.demo.repositories.UserRepository;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.client.authentication.OAuth2AuthenticationToken;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.security.web.authentication.SimpleUrlAuthenticationSuccessHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Optional;
import java.util.UUID;

@Component
public class OAuth2LoginSuccessHandler extends SimpleUrlAuthenticationSuccessHandler {

    private final UserRepository userRepository;
    private final JWTService jwtService;

    // Now hosted seamlessly by Spring Boot!
    private final String FRONTEND_URL = "/user_dashboard.html";

    public OAuth2LoginSuccessHandler(UserRepository userRepository, JWTService jwtService) {
        this.userRepository = userRepository;
        this.jwtService = jwtService;
    }

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response, Authentication authentication) throws IOException, ServletException {
        OAuth2AuthenticationToken token = (OAuth2AuthenticationToken) authentication;
        OAuth2User oAuth2User = token.getPrincipal();

        // Microsoft personal/work accounts handle email differently
        // Try multiple attribute names in order of preference
        String email = oAuth2User.getAttribute("email");
        if (email == null) {
            email = oAuth2User.getAttribute("preferred_username");
        }
        if (email == null) {
            email = oAuth2User.getAttribute("userPrincipalName");
        }
        if (email == null) {
            // Fallback: use the sub (unique ID) as a synthetic identifier
            email = oAuth2User.getAttribute("sub") + "@microsoft.oauth";
        }

        Optional<User> userOptional = userRepository.findByEmail(email);
        User user;
        boolean isNewUser = false;
        if (userOptional.isPresent()) {
            user = userOptional.get();
        } else {
            // New user signed up via OAuth2, create them in database
            isNewUser = true;
            user = new User();
            user.setEmail(email);
            user.setPassword(UUID.randomUUID().toString()); // Secure random dummy password
            userRepository.save(user);
        }

        // Create JWT token for the frontend to consume
        String jwtToken = jwtService.generateToken(user);

        // Redirect browser to frontend passing the token securely
        // Also pass whether this was a new signup or an existing user login
        String targetUrl = FRONTEND_URL + "?token=" + jwtToken + "&new_user=" + isNewUser;
        getRedirectStrategy().sendRedirect(request, response, targetUrl);
    }
}
