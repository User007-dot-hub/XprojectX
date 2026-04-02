# Phase 2 Research: Frontend Dashboard & Visualization

## Objective
Determine the best tools and charting libraries for a clean, modern, and highly responsive frontend dashboard under the constraints: React (Vite) and Vanilla CSS (no Tailwind).

## Findings
1. **Charting Library**:
   - *Option A: Recharts*. Composable React components, easy to style with CSS, lightweight.
   - *Option B: Chart.js (with react-chartjs-2)*. Canvas-based, highly performant for many data points, but slightly harder to style via CSS variables.
   - *Option C: Lightweight Charts (TradingView)*. Great for financial time-series.
   *Decision*: We will use **Recharts** for the price charts because it plays well with React components and is easy to style with our custom Vanilla CSS theme. It also handles basic time series requirements well enough for a high-level dashboard.

2. **Styling Approach (Vanilla CSS)**:
   - Since we must use Vanilla CSS (as per SPEC), we will use CSS variables (`:root`) to define a comprehensive design system (colors, spacing, typography).
   - We will implement a "glassmorphism" or sleek dark mode to meet the "rich aesthetics" requirement.

3. **API Integration**:
   - Native `fetch` API will be used to keep dependencies low. No need for Axios.
   - We need endpoints from Phase 1: `POST /api/predict`, `GET /api/stock/{ticker}`.

4. **Routing**:
   - A single-page dashboard does not strictly require `react-router-dom` unless we have multiple distinct pages. For this app, a single dashboard layout is sufficient. We will skip the router to keep it simple, or use state-based rendering.
