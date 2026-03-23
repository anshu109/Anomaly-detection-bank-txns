# Anomaly detection in bank transactions 
# Transaction Log Anomaly Detection

## Overview

This project focuses on detecting anomalous financial transactions from semi-structured logs.

The main challenge was handling inconsistent log formats and extracting meaningful signals for anomaly detection.

---

## Parsing Approach

The logs were not uniform and appeared in multiple formats (e.g. "::", "|", ">>", key-value pairs). 

Instead of forcing a single parsing rule, I handled each format separately and skipped malformed entries.

This made the parsing step more reliable and closer to how real-world log pipelines are built.

---

## Feature Engineering

Features were designed around user behavior:

- Relative transaction amount (vs user average)
- Device change between transactions
- Geographic movement (city-level approximation)
- Transaction frequency within short intervals
- Time-based features (night activity)

Additionally, velocity-based features (distance / time) were used to detect unrealistic movement patterns.

---

## Modeling Approach

I used a combination of:

1. Isolation Forest (unsupervised anomaly detection)
2. Rule-based scoring (domain-driven logic)

This hybrid setup helps balance statistical detection with interpretable signals.

---

## Key Findings

- Large location jumps within short time windows were the strongest anomaly signal
- High-value transactions relative to user history were consistently flagged
- Device changes alone were weak signals but useful when combined with others

---

## Limitations

- No labeled data for quantitative evaluation
- Location mapped at city level (not precise)
- Some logs were incomplete or malformed

---

## Business Impact

This approach can help:

- Prioritize high-risk transactions for manual review
- Reduce fraud investigation time
- Provide explainable alerts instead of black-box outputs

---

## Optional Improvements

- Use real geolocation APIs for precision
- Add sequence-based models for user behavior
- Deploy as a real-time scoring service
