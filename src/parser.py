import io
import pandas as pd
from typing import Tuple


def parse_screentime_csv(file) -> Tuple[pd.DataFrame, str]:
    """Parse a Screen Time CSV export (or similar) and return a normalized DataFrame.

    The parser attempts to be forgiving about column names. It returns a DataFrame
    with columns: `date` (datetime.date), `app` (str), `minutes` (float).
    """
    # Accept either path-like or BytesIO / uploaded file
    if hasattr(file, 'read'):
        content = file.read()
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')
        df = pd.read_csv(io.StringIO(content))
    else:
        df = pd.read_csv(file)

    cols = {c.lower(): c for c in df.columns}

    # Heuristics for columns
    date_col = None
    app_col = None
    minutes_col = None

    for name_l, orig in cols.items():
        if 'date' in name_l or 'day' in name_l:
            date_col = orig
        if 'app' in name_l or 'bundle' in name_l or 'category' in name_l:
            # prefer explicit app column
            if 'app' in name_l:
                app_col = orig
            elif app_col is None:
                app_col = orig
        if 'min' in name_l or 'minutes' in name_l or 'duration' in name_l or 'usage' in name_l:
            minutes_col = orig

    # Fallbacks
    if date_col is None:
        # try first column
        date_col = df.columns[0]
    if app_col is None:
        # try second column
        app_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    if minutes_col is None:
        # try last column
        minutes_col = df.columns[-1]

    # Convert date
    try:
        df['date'] = pd.to_datetime(df[date_col]).dt.date
    except Exception:
        # if parsing fails, leave raw
        df['date'] = df[date_col]

    # Normalize minutes column: try to extract numbers
    def to_minutes(x):
        try:
            return float(x)
        except Exception:
            s = str(x)
            # try hh:mm
            if ':' in s:
                parts = s.split(':')
                try:
                    h = float(parts[0])
                    m = float(parts[1])
                    return h * 60 + m
                except Exception:
                    return 0.0
            # strip non-digits
            import re
            m = re.findall(r"[0-9]+(?:\.[0-9]+)?", s)
            return float(m[0]) if m else 0.0

    df['minutes'] = df[minutes_col].apply(to_minutes)
    df['app'] = df[app_col].astype(str)

    out = df[['date', 'app', 'minutes']].copy()
    return out, "parsed"


if __name__ == '__main__':
    # quick smoke test with sample file
    sample = 'c:\\Users\\ranvi\\OneDrive\\Documents\\Iphone_Dashboard_Agentic_Dashboard\\sample_data\\your_screentime.csv'
    df, _ = parse_screentime_csv(sample)
    print(df.head())
