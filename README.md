# iPhone Screen Time Dashboard (Streamlit)

A simple web dashboard that turns an iPhone Screen Time export (CSV) into charts —
which apps you use the most, how your usage changes day to day, and totals for a
chosen date range. Built with [Streamlit](https://streamlit.io), pandas, and Plotly.

## How this project came together

1. Wrote the app in Python: [src/parser.py](src/parser.py) reads the CSV and cleans it up
   into a simple `date, app, minutes` table, and [src/app.py](src/app.py) uses Streamlit to
   turn that table into filters, stats, and charts.
2. Pushed the code to a GitHub repo (this one) so it's version-controlled and shareable.
3. **Future plan:** connect this GitHub repo to [Streamlit Community Cloud](https://share.streamlit.io),
   so it auto-installs `requirements.txt` and runs the app on their servers, giving anyone with
   the link a live version, with no setup on their end. Not done yet, so for now, running it means
   following the local setup below.

## Tools used

- **Python** — the programming language everything is written in.
- **pandas** — reads and reshapes the CSV data into a table the app can work with.
- **Plotly** — draws the interactive charts (bar chart, line charts).
- **Streamlit** — turns the Python script into a web page with filters, buttons, and charts, no HTML/CSS needed.
- **GitHub** — stores and version-controls the code, and is where a hosted version will eventually deploy from.

## Run it yourself

If you'd rather run the code locally instead of using the hosted link, clone the repo and
run these commands in a terminal, in order:

```bash
git clone https://github.com/rpatil09/Iphone-Dashboard-AIProject.git
cd Iphone-Dashboard-AIProject        # now inside the project root, everything below runs from here

python -m venv .venv
.venv\Scripts\activate               # Windows — on Mac/Linux use: source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```

This opens the dashboard at `http://localhost:8501` in your browser.

## Usage

- The app loads `sample_data/your_screentime.csv` automatically — this is real Screen Time
  export data, not a placeholder.
- The app shows total usage by app and usage over time.