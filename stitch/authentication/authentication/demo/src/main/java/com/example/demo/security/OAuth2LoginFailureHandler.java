package com.example.demo.security;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.authentication.AuthenticationFailureHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

@Component
public class OAuth2LoginFailureHandler implements AuthenticationFailureHandler {

    @Override
    public void onAuthenticationFailure(HttpServletRequest request, HttpServletResponse response, AuthenticationException exception) throws IOException, ServletException {
        System.err.println("===== OAUTH2 LOGIN FAILED =====");
        System.err.println("REASON: " + exception.getMessage());
        exception.printStackTrace();
        
        // Pass the error back to the frontend to alert the user
        String errorMsg = exception.getMessage() != null ? exception.getMessage() : "Unknown_OAuth2_Error";
        String encodedError = URLEncoder.encode(errorMsg, StandardCharsets.UTF_8.toString());
        response.sendRedirect("http://localhost:8080/final_login_page.html?oauth_error=" + encodedError);
    }
}
