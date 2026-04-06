package com.example.demo.repositories;

import com.example.demo.models.DashboardCalculation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DashboardCalculationRepository extends JpaRepository<DashboardCalculation, Long> {
    List<DashboardCalculation> findByUserEmailOrderByCreatedAtDesc(String email);
}
