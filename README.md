# iPhone Screen Time Dashboard (Streamlit)

Simple Streamlit dashboard to visualize iPhone Screen Time exports (CSV). Minimal parser + sample data included.

Quick start

1. Create a Python venv and install requirements:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the app:

```bash
streamlit run src/app.py
```

Usage

- Upload your exported Screen Time CSV, or use the included sample under `sample_data`.
- The app shows total usage by app and usage over time.

Notes

- If your Screen Time export has different column names, open `src/parser.py` and adapt the mapping.