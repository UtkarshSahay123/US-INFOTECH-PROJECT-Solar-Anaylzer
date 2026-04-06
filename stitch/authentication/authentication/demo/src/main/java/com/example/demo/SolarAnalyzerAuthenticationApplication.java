package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.persistence.autoconfigure.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication


@EnableJpaRepositories(basePackages = "com.example.demo.repositories") // <-- Ye Line Jodein
@EntityScan(basePackages = "com.example.demo.models")// <-- Ye Line Jodein



public class SolarAnalyzerAuthenticationApplication {

	public static void main(String[] args) {
		SpringApplication.run(SolarAnalyzerAuthenticationApplication.class, args);
	}

}
