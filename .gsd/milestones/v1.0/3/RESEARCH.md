# Phase 3 Research: Education Chatbot

## Tech Stack Context
* **Backend**: FastAPI, `google-generativeai` (already present in `requirements.txt`).
* **Frontend**: React, Vanilla CSS. `lucide-react` for icons.

## API Integration Strategy
Google Generative AI provides the current robust SDK for interacting with Gemini models.
- **Model**: `gemini-1.5-flash` is best for chat and responsive performance at zero cost.
- **Constraints**: We need to ensure the bot is strictly scoped to finance/investing. This will be enforced via a `system_instruction` in the model configuration to refuse non-financial questions.
- **Endpoints**: A `POST /api/chat` route that expects a list of messages (history) and a new user message.

## UI/UX Considerations
* Chat must be accessible from the dashboard without obfuscating the charts or prediction inputs.
* **Component Approach**: A floating action button (FAB) opening a slide-out side panel (`ChatPanel.jsx`) with a backdrop blur is ideal.
* State management will hold conversational history in standard React state.

## Level 1 Discovery Result
Confirmed `gemini-1.5-flash` is supported, `google-generativeai` is available, and an isolated slide-out side panel provides the best premium UX for the dashboard.
