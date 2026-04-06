package com.example.demo.models;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "dashboard_calculations")
public class DashboardCalculation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    private Double detectedAreaM2;
    private Double systemCapacityKw;
    private Integer maxPanels;
    private String panelDimensions;
    private Double dailyEnergyKwh;
    private Double monthlyEnergyKwh;
    private Double monthlyProfitUsd;
    private String currencyCode;      // e.g. "INR", "USD", "EUR"
    private String currencySymbol;    // e.g. "₹", "$", "€"
    
    private Double temperatureCelsius;
    private Double windspeedKmh;
    private String sunrise;
    private String sunset;
    @Column(length = 1000)
    private String userComment;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    public DashboardCalculation() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }

    public Double getDetectedAreaM2() { return detectedAreaM2; }
    public void setDetectedAreaM2(Double detectedAreaM2) { this.detectedAreaM2 = detectedAreaM2; }

    public Double getSystemCapacityKw() { return systemCapacityKw; }
    public void setSystemCapacityKw(Double systemCapacityKw) { this.systemCapacityKw = systemCapacityKw; }

    public Integer getMaxPanels() { return maxPanels; }
    public void setMaxPanels(Integer maxPanels) { this.maxPanels = maxPanels; }

    public String getPanelDimensions() { return panelDimensions; }
    public void setPanelDimensions(String panelDimensions) { this.panelDimensions = panelDimensions; }

    public Double getDailyEnergyKwh() { return dailyEnergyKwh; }
    public void setDailyEnergyKwh(Double dailyEnergyKwh) { this.dailyEnergyKwh = dailyEnergyKwh; }

    public Double getMonthlyEnergyKwh() { return monthlyEnergyKwh; }
    public void setMonthlyEnergyKwh(Double monthlyEnergyKwh) { this.monthlyEnergyKwh = monthlyEnergyKwh; }

    public Double getMonthlyProfitUsd() { return monthlyProfitUsd; }
    public void setMonthlyProfitUsd(Double monthlyProfitUsd) { this.monthlyProfitUsd = monthlyProfitUsd; }

    public String getCurrencyCode() { return currencyCode; }
    public void setCurrencyCode(String currencyCode) { this.currencyCode = currencyCode; }

    public String getCurrencySymbol() { return currencySymbol; }
    public void setCurrencySymbol(String currencySymbol) { this.currencySymbol = currencySymbol; }

    public Double getTemperatureCelsius() { return temperatureCelsius; }
    public void setTemperatureCelsius(Double temperatureCelsius) { this.temperatureCelsius = temperatureCelsius; }

    public Double getWindspeedKmh() { return windspeedKmh; }
    public void setWindspeedKmh(Double windspeedKmh) { this.windspeedKmh = windspeedKmh; }

    public String getSunrise() { return sunrise; }
    public void setSunrise(String sunrise) { this.sunrise = sunrise; }

    public String getSunset() { return sunset; }
    public void setSunset(String sunset) { this.sunset = sunset; }

    public String getUserComment() { return userComment; }
    public void setUserComment(String userComment) { this.userComment = userComment; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
