package com.example.demo.security; // Apne hisab se package name adjust karein ya security package me dalein

import com.example.demo.models.User;
import com.example.demo.repositories.UserRepository;
import com.example.demo.security.JWTService;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final com.example.demo.security.JWTService jwtService;
    private final AuthenticationManager authenticationManager;

    // Constructor Injection (Spring Boot automatically injects these dependencies)
    public AuthService(UserRepository userRepository,
                       PasswordEncoder passwordEncoder,
                       com.example.demo.security.JWTService jwtService,
                       AuthenticationManager authenticationManager) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
        this.authenticationManager = authenticationManager;
    }

    // --- 1. SIGN UP (REGISTER) ---
    public String register(String email, String rawPassword) {
        // Check if user already exists
        if (userRepository.existsByEmail(email)) {
            throw new RuntimeException("Error: Email is already in use!");
        }

        // Hash the password securely and save the user
        User user = new User();
        user.setEmail(email);
        user.setPassword(passwordEncoder.encode(rawPassword));

        userRepository.save(user);

        // Generate the token so they are instantly logged in
        return jwtService.generateToken(user);
    }

    // --- 2. LOG IN ---
    public String authenticate(String email, String rawPassword) {
        // This will check if username and password match. If they don't, it throws an exception.
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(email, rawPassword)
        );

        // If we reach here, password was correct. Load user and generate token.
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));

        return jwtService.generateToken(user);
    }
}
