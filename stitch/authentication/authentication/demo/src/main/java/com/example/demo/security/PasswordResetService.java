package com.example.demo.security;

import com.example.demo.models.User;
import com.example.demo.repositories.UserRepository;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.Random;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class PasswordResetService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JavaMailSender mailSender;

    // In-memory OTP storage: email -> OtpData
    private final ConcurrentHashMap<String, OtpData> otpStore = new ConcurrentHashMap<>();

    public PasswordResetService(UserRepository userRepository, PasswordEncoder passwordEncoder, JavaMailSender mailSender) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.mailSender = mailSender;
    }

    // --- Generate and send OTP ---
    public boolean sendOtp(String email) {
        Optional<User> userOpt = userRepository.findByEmail(email);
        if (userOpt.isEmpty()) {
            return false; // User not registered
        }

        // Generate 6-digit OTP
        String otp = String.format("%06d", new Random().nextInt(999999));

        // Store with 5-minute expiry
        otpStore.put(email.toLowerCase(), new OtpData(otp, LocalDateTime.now().plusMinutes(5)));

        // Send email
        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom("utkarshsahay321@gmail.com");
        message.setTo(email);
        message.setSubject("SolarPulse - Password Reset OTP");
        message.setText(
            "Hello,\n\n" +
            "Your OTP for password reset is: " + otp + "\n\n" +
            "This code is valid for 5 minutes.\n\n" +
            "If you did not request this, please ignore this email.\n\n" +
            "- SolarPulse Team"
        );

        try {
            mailSender.send(message);
            System.out.println("[OTP] Sent OTP " + otp + " to " + email); // Console backup for debugging
            return true;
        } catch (Exception e) {
            System.err.println("[OTP] Failed to send email: " + e.getMessage());
            return false;
        }
    }

    // --- Verify OTP ---
    public boolean verifyOtp(String email, String otp) {
        OtpData data = otpStore.get(email.toLowerCase());
        if (data == null) return false;
        if (LocalDateTime.now().isAfter(data.expiry)) {
            otpStore.remove(email.toLowerCase()); // Expired, clean up
            return false;
        }
        return data.otp.equals(otp);
    }

    // --- Reset Password ---
    public void resetPassword(String email, String otp, String newPassword) {
        // Re-verify OTP before changing password
        if (!verifyOtp(email, otp)) {
            throw new IllegalArgumentException("Failed to reset password. Invalid or expired OTP.");
        }

        Optional<User> userOpt = userRepository.findByEmail(email);
        if (userOpt.isEmpty()) {
            throw new IllegalArgumentException("User not found.");
        }

        User user = userOpt.get();
        
        // Ensure new password isn't the same as the old password
        if (passwordEncoder.matches(newPassword, user.getPassword())) {
            throw new IllegalArgumentException("Your new password cannot be the same as your old password.");
        }

        user.setPassword(passwordEncoder.encode(newPassword));
        userRepository.save(user);

        // Consume OTP so it can't be reused
        otpStore.remove(email.toLowerCase());
    }

    // --- Internal OTP data holder ---
    private static class OtpData {
        String otp;
        LocalDateTime expiry;

        OtpData(String otp, LocalDateTime expiry) {
            this.otp = otp;
            this.expiry = expiry;
        }
    }
}
