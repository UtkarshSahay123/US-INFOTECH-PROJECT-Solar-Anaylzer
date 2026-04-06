package com.example.demo.controllers;

import com.example.demo.models.DashboardCalculation;
import com.example.demo.models.User;
import com.example.demo.repositories.DashboardCalculationRepository;
import com.example.demo.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/dashboard")
@CrossOrigin(origins = "*")
public class DashboardController {

    @Autowired
    private DashboardCalculationRepository calculationRepository;

    @Autowired
    private UserRepository userRepository;

    @PostMapping("/save")
    public ResponseEntity<?> saveCalculation(@RequestBody DashboardCalculation calculation, Authentication authentication) {
        if (authentication == null || !authentication.isAuthenticated()) {
            return ResponseEntity.status(401).body("Unauthorized");
        }

        com.example.demo.models.User currentUser = null;
        Object principal = authentication.getPrincipal();
        if (principal instanceof com.example.demo.models.User) {
            currentUser = (com.example.demo.models.User) principal;
        } else {
            String userEmail = authentication.getName();
            currentUser = userRepository.findByEmail(userEmail).orElse(null);
        }
        
        if (currentUser == null) {
            return ResponseEntity.status(401).body("{\"error\": \"User not found in database. Session invalid.\"}");
        }

        calculation.setUser(currentUser);
        DashboardCalculation saved = calculationRepository.save(calculation);
        
        return ResponseEntity.ok(saved);
    }

    @GetMapping("/history")
    public ResponseEntity<?> getHistory(Authentication authentication) {
        if (authentication == null || !authentication.isAuthenticated()) {
            return ResponseEntity.status(401).body("Unauthorized");
        }

        String userEmail = authentication.getName();
        List<DashboardCalculation> history = calculationRepository.findByUserEmailOrderByCreatedAtDesc(userEmail);
        
        return ResponseEntity.ok(history);
    }

    @DeleteMapping("/history/{id}")
    public ResponseEntity<?> deleteHistoryItem(@PathVariable Long id, Authentication authentication) {
        if (authentication == null || !authentication.isAuthenticated()) {
            return ResponseEntity.status(401).body("Unauthorized");
        }

        Optional<DashboardCalculation> calcOpt = calculationRepository.findById(id);
        if (calcOpt.isEmpty()) {
            return ResponseEntity.status(404).body("Calculation not found");
        }

        DashboardCalculation calc = calcOpt.get();
        if (!calc.getUser().getEmail().equals(authentication.getName())) {
            return ResponseEntity.status(403).body("Forbidden");
        }

        calculationRepository.deleteById(id);
        return ResponseEntity.ok().body("{\"message\": \"Deleted successfully\"}");
    }
}
