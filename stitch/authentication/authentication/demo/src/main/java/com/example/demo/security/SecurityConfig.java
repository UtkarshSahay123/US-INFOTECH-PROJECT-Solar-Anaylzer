package com.example.demo.security;


import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;


@Configuration
@EnableWebSecurity
public class SecurityConfig {
    private final JwtAuthenticationFilter jwtAuthFilter;
    private final OAuth2LoginSuccessHandler oAuth2LoginSuccessHandler;
    private final OAuth2LoginFailureHandler oAuth2LoginFailureHandler;
    private final ApiAuthenticationEntryPoint apiAuthenticationEntryPoint;

    public SecurityConfig(JwtAuthenticationFilter jwtAuthFilter,
                          OAuth2LoginSuccessHandler oAuth2LoginSuccessHandler,
                          OAuth2LoginFailureHandler oAuth2LoginFailureHandler,
                          ApiAuthenticationEntryPoint apiAuthenticationEntryPoint) {
        this.jwtAuthFilter = jwtAuthFilter;
        this.oAuth2LoginSuccessHandler = oAuth2LoginSuccessHandler;
        this.oAuth2LoginFailureHandler = oAuth2LoginFailureHandler;
        this.apiAuthenticationEntryPoint = apiAuthenticationEntryPoint;
    }
    // 1. Kon sa URL allow karna hai aur kon sa nahi
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http,org.springframework.security.authentication.AuthenticationProvider authenticationProvider) throws Exception {
        http
                .cors(cors -> cors.configurationSource(request -> {
                    org.springframework.web.cors.CorsConfiguration config = new org.springframework.web.cors.CorsConfiguration();
                    config.setAllowedOrigins(java.util.List.of("*"));
                    config.setAllowedMethods(java.util.List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
                    config.setAllowedHeaders(java.util.List.of("*"));
                    return config;
                }))
                .csrf(AbstractHttpConfigurer::disable) // Postman se hit marne ke liye disable karte hain
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers(
                            "/api/auth/**", 
                            "/login/**", 
                            "/oauth2/**", 
                            "/*.html", 
                            "/**/*.html", 
                            "/**/*.css", 
                            "/**/*.js", 
                            "/**/*.png", 
                            "/**/*.jpg", 
                            "/assets/**", 
                            "/images/**",
                            "/"
                        ).permitAll() // Login aur Signup kisi bhi user ke liye allow!
                        .anyRequest().authenticated()                // Dusra koi bhi URL ho ("/user_dashboard"), pehle login!
                )
                .oauth2Login(oauth2 -> oauth2
                        .loginPage("/final_login_page.html")
                        .successHandler(oAuth2LoginSuccessHandler)
                        .failureHandler(oAuth2LoginFailureHandler)
                )
                .formLogin(form -> form
                        .loginPage("/final_login_page.html")
                        .permitAll()
                )
                .sessionManagement(sess -> sess.sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)) // OAuth2 needs session for state param; JWTs handle API auth

                .exceptionHandling(ex -> ex
                        .authenticationEntryPoint(apiAuthenticationEntryPoint)
                )
                .authenticationProvider(authenticationProvider)
                .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }

}
