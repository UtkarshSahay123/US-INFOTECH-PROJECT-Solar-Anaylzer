package com.example.demo.models;

import jakarta.persistence.*;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.List;

@Entity
@Table(name = "users")
public class User implements UserDetails {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; // Using Long (wrapper) is best practice for JPA IDs

    @Column(unique = true, nullable = false)
    private String email;

    @Column(nullable = false)
    private String password;

    // --- Constructors ---
    public User() {}

    public User(String email, String password) {
        this.email = email;
        this.password = password;
    }

    // --- Getters & Setters ---
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    // --- UserDetails Overrides ---

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of(); // Return empty list initially (no specific admin/user roles yet)
    }

    @Override
    public String getUsername() {
        return this.email; // Spring Security uses email as the login identity
    }

    @Override
    public String getPassword() {
        return this.password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}
