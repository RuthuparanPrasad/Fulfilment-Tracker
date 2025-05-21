# Apprentice Fulfilment Tracker Dashboard

This project is an end-to-end automated data pipeline and dashboard that tracks apprentice fulfilment progress using real-time (sample) data from Google Sheets.

It includes:
- 📄 Dynamic data extraction from Google Sheets using Python and `gspread`
- 🧹 Data cleaning and transformation (e.g. tracking days to diagnostic, assignment, and onboarding)
- 💾 Local storage into a SQLite database (`fulfilment_tracker.db`)
- 📊 A fully interactive Metabase dashboard running on Docker
- 🖥 One-click Python script (`run_dashboard.py`) to process data, launch Metabase, and open the dashboard on `localhost:3000`

This is ideal for demoing how data automation and self-serve analytics can be deployed quickly and effectively.

---

### 🚀 How to Run Locally

1. Clone this repo
2. Add your `creds.json` file or set `GOOGLE_CREDS_JSON` as an environment variable
3. Run:
   ```bash
   python run_dashboard.py
