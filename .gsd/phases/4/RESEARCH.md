# Phase 4 Research: Retraining & Polish

## Current State Analysis
* **Backend**: An endpoint `POST /api/retrain` ALREADY exists in `backend/app/routers/prediction.py`. It correctly executes `ml_service.train` and returns fresh metrics.
* **Frontend**: The `fetch` payload targets in `App.jsx` and `ChatPanel.jsx` are currently hardcoded strictly to `http://localhost:8000`. 
* **User Interface**: For REQ-13, we need a "Retrain" button prominently displayed when a user interacts with a prediction, empowering them to manually force the model to ingest fresh data today without disrupting the UI flow.

## Proposed Strategy
1. **Frontend Retraining UI**: Inject a "Retrain Model" button inside `PredictionResult.jsx` utilizing `lucide-react` Refresh icons. Upon clicking, we toggle an `isRetraining` loading layout, execute the `/api/retrain` endpoint, and seamlessly re-fire the original `/api/predict` routine so the view cleanly shifts to the updated prediction.
2. **Environment Configuration (Deployment Polish)**: Create a `.env` schema inside `frontend/` deploying `VITE_API_URL=http://localhost:8000/api`. We refactor all raw strings to map to `import.meta.env.VITE_API_URL` dynamically, defaulting to relative paths (`/api`) to ease arbitrary production deployment.
3. **General Polish**: Enhance any unresolved disabled UI states (locking forms cleanly during async work) and polish Vite native elements (document `<title>`).

## Discovery Level 1
Architecture review confirms all necessary backend mechanisms for Retraining are functional; focus is strictly on extending the React app UI and structuring environment variables for Phase 4 closure.
