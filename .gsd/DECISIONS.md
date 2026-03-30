# DECISIONS.md — Architecture Decision Records

## Format

Each decision follows this format:
- **ID**: ADR-{N}
- **Date**: YYYY-MM-DD
- **Decision**: What was decided
- **Rationale**: Why this choice was made
- **Alternatives**: What else was considered

---

## ADR-01: Tech Stack Selection
**Date**: 2026-03-31
**Decision**: FastAPI (backend) + React/Vite (frontend) + scikit-learn (ML) + yfinance (data) + Gemini (chatbot)
**Rationale**: Simplest stack that covers all requirements. FastAPI is async and great for ML serving. React is component-based and well-documented. scikit-learn is sufficient for classification tasks. yfinance is free with no API key. Gemini has a free tier.
**Alternatives**: Flask (less async support), Django (too heavy), TensorFlow/PyTorch (overkill for this task), Alpha Vantage (requires API key)

## ADR-02: No User Authentication
**Date**: 2026-03-31
**Decision**: No login or user accounts. Open access to all features.
**Rationale**: Adds complexity with no benefit at this stage. No user-specific data needs to be persisted. Can be added later if needed.
**Alternatives**: JWT auth, OAuth — deferred to future milestone.

## ADR-03: Manual Retraining Only
**Date**: 2026-03-31
**Decision**: Single "Retrain" button that fetches fresh data and retrains the model on demand.
**Rationale**: Automatic retraining requires job scheduling infrastructure (Celery, cron, etc.) which is unnecessary complexity at v1.0. Manual retraining is honest, functional, and teachable.
**Alternatives**: Scheduled retraining (cron), online learning — deferred.
