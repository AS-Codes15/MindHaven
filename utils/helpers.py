from datetime import datetime

def pretty_ts(ts: str) -> str:
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%b %d, %Y %H:%M")
    except Exception:
        return ts
