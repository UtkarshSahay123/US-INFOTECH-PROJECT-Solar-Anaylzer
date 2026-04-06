package com.example.demo.repositories;
import com.example.demo.models.User;
import org.springframework.data.jpa.repository.JpaRepository;

import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {



    // Email ke through user dhoondne ke liye
    Optional<User> findByEmail(String email);

    // Check karne ke liye ki email database me hai ya nahi
    boolean existsByEmail(String email);
}
