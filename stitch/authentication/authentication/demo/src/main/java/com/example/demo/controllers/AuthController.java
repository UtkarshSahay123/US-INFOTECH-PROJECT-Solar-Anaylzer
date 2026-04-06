package com.example.demo.controllers; // Pura package dekh lijiye (eg. com.example.demo.controllers)


import com.example.demo.security.AuthService;
import com.example.demo.security.PasswordResetService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@CrossOrigin("*")
@RestController
@RequestMapping("/api/auth") // Postman par base URL yahi hoga!
public class AuthController {

    private final AuthService authService;
    private final PasswordResetService passwordResetService;

    // Constructor Injection
    public AuthController(AuthService authService, PasswordResetService passwordResetService) {
        this.authService = authService;
        this.passwordResetService = passwordResetService;
    }

    // 1. SIGNUP API
    // Request aaega: POST http://localhost:8080/api/auth/signup
    @PostMapping("/signup")
    public ResponseEntity<?> register(@RequestBody LoginSignupRequest request) {
        try {
            // AuthService ko bulao aur usko email/password the dho
            String token = authService.register(request.getEmail(), request.getPassword());

            // Agar sab thik raha, toh naya JWT Token user ko wapas de do
            return ResponseEntity.ok(Map.of("token", token, "message", "User registered successfully!"));
        } catch (RuntimeException e) {
            // Agar email pehle se hai, toh Error message dikhao
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    // 2. LOGIN API
    // Request aaega: POST http://localhost:8080/api/auth/login
    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginSignupRequest request) {
        try {
            // Login check karo aur naya Token lao
            String token = authService.authenticate(request.getEmail(), request.getPassword());
            return ResponseEntity.ok(Map.of("token", token, "message", "Login successful!"));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(Map.of("error", "Invalid email or password"));
        }
    }

    // 3. FORGOT PASSWORD - Send OTP to email
    @PostMapping("/forgot-password")
    public ResponseEntity<?> forgotPassword(@RequestBody ForgotPasswordRequest request) {
        boolean sent = passwordResetService.sendOtp(request.getEmail());
        if (sent) {
            return ResponseEntity.ok(Map.of("message", "OTP sent to your email"));
        } else {
            return ResponseEntity.badRequest().body(Map.of("error", "Email not registered"));
        }
    }

    // 4. VERIFY OTP
    @PostMapping("/verify-otp")
    public ResponseEntity<?> verifyOtp(@RequestBody VerifyOtpRequest request) {
        boolean valid = passwordResetService.verifyOtp(request.getEmail(), request.getOtp());
        if (valid) {
            return ResponseEntity.ok(Map.of("message", "OTP verified successfully"));
        } else {
            return ResponseEntity.badRequest().body(Map.of("error", "Invalid or expired OTP"));
        }
    }

    // 5. RESET PASSWORD
    @PostMapping("/reset-password")
    public ResponseEntity<?> resetPassword(@RequestBody ResetPasswordRequest request) {
        try {
            passwordResetService.resetPassword(request.getEmail(), request.getOtp(), request.getNewPassword());
            return ResponseEntity.ok(Map.of("message", "Password reset successfully"));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    // --- DTO Classes ---
    public static class LoginSignupRequest {
        private String email;
        private String password;

        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }

        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }
    }

    public static class ForgotPasswordRequest {
        private String email;
        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }
    }

    public static class VerifyOtpRequest {
        private String email;
        private String otp;
        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }
        public String getOtp() { return otp; }
        public void setOtp(String otp) { this.otp = otp; }
    }

    public static class ResetPasswordRequest {
        private String email;
        private String otp;
        private String newPassword;
        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }
        public String getOtp() { return otp; }
        public void setOtp(String otp) { this.otp = otp; }
        public String getNewPassword() { return newPassword; }
        public void setNewPassword(String newPassword) { this.newPassword = newPassword; }
    }
}
