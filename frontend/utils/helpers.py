def confidence_label(score: float) -> tuple[str, str]:
    """Return (label, hex_color) based on a 0-1 confidence score."""
    if score >= 0.7:
        return "High", "#22c55e"
    elif score >= 0.4:
        return "Medium", "#f59e0b"
    else:
        return "Low", "#ef4444"


def truncate(text: str, max_len: int = 180) -> str:
    """Truncate text for preview display."""
    if len(text) <= max_len:
        return text
    return text[:max_len].rstrip() + "..."


def total_pipeline_time(timing: dict) -> float:
    """Sum all agent timings into a total pipeline duration."""
    return round(sum(timing.values()), 2)


def load_css(path: str) -> str:
    """Read a CSS file and return its content."""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""
